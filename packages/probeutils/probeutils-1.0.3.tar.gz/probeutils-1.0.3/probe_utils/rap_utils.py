from Bio.Seq import Seq
from gget import blat

import pandas as pd
import numpy as np

from tqdm import tqdm

import sys
import os
import time
import threading
import requests

class Spinner:
    '''
    Spinning progress wheel used for DFAM step
    Taken from: https://stackoverflow.com/questions/4995733/
    how-to-create-a-spinning-command-line-cursor
    
    '''
    
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False
        
def blatfilt(seq,
             genome,
             probels,
             log=None,
             tolerance=25):
    '''
    Runs UCSC Blat to remove probes with off-target homology
    
    Parameters
    __________
    
    seq : str
        Full length of transcript sequence
        
    genome : str
        Short assembly name for the species genome as listed in BLAT, 
        e.g. 'hg38,' 'mm39,' or 'dm6'
        
    probels : list of strings
        List of probes to be analyzed
        
    log : file object or None
        Log file to store BLAT progress. If None, blatfilt() 
        will generate a log file. If open file object, BLAT will
        append to an existing text file.
        
    tolerance : int
        Number of acceptable matches to other genomic loc. Default 25
        
    Returns
    _______
    
    output : two dataframes
        BLAT results for probes that passed thresholds and those that
        did not
        
    '''
    # Generate log if needed
    if log == None:
        log = open('blatFiltLog.out','w')   
    else:
        pass
    
    # BLAT full sequence to identify gene location
    if len(seq) > 8000:
        seqloc = blat(seq[:8000], assembly=genome, verbose=False).loc[0]
        endhandle = blat(seq[-1000:], assembly=genome, verbose=False).loc[0]
        if seqloc['strand'] == '+':
            seqloc['end'] = endhandle['end']
        else:
            seqloc['start'] = endhandle['start']
    else:
        seqloc = blat(seq, assembly=genome, verbose=False).loc[0]
    
    # Update log with gene location
    log.writelines('BLAT Results\n')
    
    startend = '-'.join([str(seqloc['start']),str(seqloc['end'])])
    strand = ' (' + seqloc['strand'] + ')'
    locus = seqloc['chromosome'] + ':' + startend + strand
    
    log.writelines('Identified locus: ' + locus + '\n')
    
    # Check whether entire sequence is present in the indicated genome
    percmatch = str(seqloc['%_matched']) + '%'
    log.writelines('Genome Match: ' + percmatch + '\n')
    
    if seqloc['%_matched'] != 100:
        matcherr = input('The submitted sequence had only a ' + percmatch + 
                         ' match to the target genome.\n Proceed anyway? [Y/N]')
        if matcherr == 'Y':
            log.writelines('Continued with BLAT filtering\n')
        else:
            log.writelines('Probe generation cancelled by user\n')
            raise Exception('Job cancelled.')
    else:
        pass
    
    # Reformat probe list for BLAT submission
    blat_ls = ['>'+str(i)+'\n'+v for i,v in enumerate(probels)]
    
    # Generate indices to comply with BLAT submission limits
    inds = list(np.arange(0,len(blat_ls),25))

    if inds[-1] != len(blat_ls):
        inds.append(len(blat_ls))

    sinds = []

    for i,v in enumerate(inds[:-1]):
        sinds.append(np.s_[v:inds[i+1]])

    # BLAT server URL
    blat_url = "https://genome.ucsc.edu/cgi-bin/hgBlat"
    
    # Make list to store dataframes for each BLAT query
    df_ls = []
    
    # Submit BLAT requests in groups of 25 sequences
    for i in tqdm(sinds):
        sequence_data='\n'.join(blat_ls[i])
        
        # Parameters for the BLAT request
        params = {
            'userSeq': sequence_data,
            'type': 'dna',
            'output': 'json',
            'db':genome
        }

        # Perform BLAT search
        response = requests.get(blat_url, params=params)
        json = response.json()

        df_ls.append(pd.DataFrame(json['blat'],columns=json['fields']))
    
    # Join dataframes for entire BLAT set
    dfall = pd.concat(df_ls)
    
    # Drop unused columns
    dropcols = ['qNumInsert',
            'qBaseInsert',
            'tNumInsert',
            'tBaseInsert',
            'strand',
            'misMatches',
            'repMatches',
            'nCount',
            'qSize',
            'qStart',
            'qEnd',
            'tSize',
            'blockCount',
            'blockSizes']
    
    dfall.drop(dropcols,axis=1,inplace=True)
    
    # Generate empty lists to store probe IDs
    keep_probes = []
    drop_probes = []

    # Generate query names
    qnames = [str(i) for i in range(len(probels))]

    # Check if all probes were run
    if all([i in np.unique(dfall['qName']) for i in qnames]):
        pass
    else:
        raise Exception('''Not all probes were successfully blatted. This is likely due to 
                        submitting too many requests to the BLAT web server. Try splitting 
                        your sequence(s) into smaller submissions.''')

    # Loop through individual probes
    chrom = seqloc['chromosome']
    for q in qnames:
        subdf = dfall[dfall['qName'] == q].copy()

        # Remove in-gene matches
        chrdf = subdf[subdf['tName'] == chrom]

        for i in chrdf.index:
            if chrdf.loc[i,'tStart'] >= seqloc['start'] and chrdf.loc[i,'tEnd'] <= seqloc['end']:
                subdf.drop(i,inplace=True)
            else:
                pass

        # Check against user-defined acceptable matches
        if all([i < tolerance for i in subdf['matches']]):
            keep_probes.append(q)
        else:
            drop_probes.append(q)

    keepdf = dfall[dfall['qName'].isin(keep_probes)]
    dropdf = dfall[dfall['qName'].isin(drop_probes)]

    return keepdf, dropdf

def dfamfilt(probels,
             species,
             directory,
             log=None):
    '''
    Runs RAP probes through DFAM database to remove 
    probes to repetitive elements
    
    Parameters
    __________
    
    probels : list of strings
        List of probes to be analyzed
        
    species : str
        DFAM species to check repeats, e.g. "Homo sapiens",
        "Mus musculus", or "Drosophila melanogaster"
        
    directory : str
        Path to the directory in which to store the results
        
    log : file object or None
        Log file to store DFAM progress. If None, dfamfilt() 
        will generate a log file. If open file object, DFAM will
        append to an existing text file.
        
    Returns
    _______
    
    output : two lists
        Lists of DFAM results for probes with repeats and those without.
        
    file : csv
        A csv containing DFAM results for probes with repeats.
        
    '''
    # Generate log file
    if log == None:
        log = open(directory + 'dfamFiltLog.out','w')   
    else:
        pass
        
    # Update log
    log.writelines('Dfam Results\n')
    
    # Submit sequences to DFAM
    url = "https://dfam.org/api/searches"
    
    ls = ['>'+str(i)+'\n'+v for i,v in enumerate(probels)]
    sequence_data = '\n'.join(ls)

    params = {'sequence':sequence_data,
              'organism':species,
              'cutoff':'curated'}
    
    # Pull submission ID
    response = requests.post(url, json=params)
    results = response.json()['id']
    
    # Retrieve submission results
    api_url = f"https://dfam.org/api/searches/{results}"

    response = requests.get(api_url)

    if response.status_code == 200:
        log.writelines('Search submitted successfully\n')
        print("Search submitted successfully.")
        # Process and use the result data as needed
    else:
        errmessage = "Failed to retrieve DFAM result. Status code: " + response.status_code
        log.writelines(errmessage + '\n')
        raise Exception(errmessage)
        
    # Dfam for multiple sequences takes some time
    # Attempt to get response until job finished
    response = requests.get(api_url)
    x = response.json()['duration']
    
    with Spinner():
        while x == 'Not finished':
            time.sleep(2)
            response = requests.get(api_url)
            x = response.json()['duration']
    
    log.writelines('Dfam search time: ' + x+ '\n')
    print('DFAM Done')
    
    results = response.json()['results']
    
    keep_probes = []
    drop_probes = []
    
    drop_dict = {'probe':[],
                 'query':[],
                 'type':[],
                 'e_value':[]}
    
    for r in results:
        if len(r['hits']) == 0:
            keep_probes.append(r['query'])
        else:
            drop_probes.append(r['query'])
            
            # Add details for export
            for i in r['hits']:
                drop_dict['probe'].append(probels[int(r['query'])])
                drop_dict['query'].append(i['query'])
                drop_dict['type'].append(i['type'])
                drop_dict['e_value'].append(i['e_value'])
                
    # Export DFAM results
    df = pd.DataFrame(drop_dict)
    df.to_csv(directory + '/dfamFailedProbes.csv',index=False)
    
    return keep_probes, drop_probes

def seq_interpreter(file):
    '''Imports sequence in a FASTA file as string
    
    Parameters
    __________
    
    file : str
        Path to FASTA file
        
    Returns
    _______
    
    output : a string
        The sequence in the FASTA file as a string. If the FASTA
        contains multiple sequences, only the first will be returned.
    
    '''
    okchars = ['A','T','C','G','a','t','c','g','\n']
    
    with open(file, 'r') as f:
        f_read = f.read()
        
    if f_read[0] != '>':
        check = [i in okchars for i in f_read]
        
        if all(check):
            seq = f_read.replace('\n','')
        else:
            raise Exception('''File not recognized as sequence. 
            If using standard FASTA, make sure the sequence name 
            begins with '>'. If only supplying sequence, make sure
            the file only contains the following characters:
            'A','T','C','G','a','t','c','g','\n''')
            
    else:
        seq = f_read.split('>')[1:]
        #print(seq)
        if len(seq) > 1:
            print('''Multiple sequences found in FASTA. Only probes 
to the first sequence will be generated.''')
            
        else:
            pass
        
        seq = seq[0].split('\n')
        seq = ''.join(seq[1:])
        
    check = [i in okchars[:-1] for i in seq]
    
    if all(check):
        pass
    else:
        raise Exception('''File not recognized as sequence. 
            If using standard FASTA, make sure the sequence name 
            begins with '>'. If only supplying sequence, make sure
            the file only contains the following characters:
            'A','T','C','G','a','t','c','g','\n''')
        
    return seq 

def rap_probes(fasta, 
               gene, 
               adaptseq = 'CAAGTCA',
               probe_length = 90,
               biotin=False,
               blat=True,
               dfam=True,
               **kwargs):
    '''Takes a sequence and makes probes of a given length
    
    Parameters
    __________
    
    fasta : str
        Path to a fasta file containing the sequence to 
        generate probes against
        
    gene : str
        The name of the target gene, used to name probes
        and the output file
        
    probe_length : int
        The total length of the probe in nucleotides. If
        an adaptor is used, this length includes the length
        of the adapter
        
    biotin : Bool
        Whether to add a 5'-biotin to the probes. Formatted
        for ordering from Integrated DNA Technologies (IDT).
        Default False
        
    blat : Bool
        Whether to filter probes for multiple genome matches 
        using UCSC BLAT. If True, the genome assembly name 
        must be supplied to **kwargs. Default True
        
    dfam : Bool
        Whether to filter probes for transposable elements and
        tandem repeats using the Institute of Systems Biology's 
        Dfam database. If True, the species name must be supplied
        to **kwargs. Default True
        
    **kwargs : dictionary
    
        genome : str
            Used for BLAT filtering. Short assembly name for the 
            species genome as listed in BLAT, e.g. 'hg38,' 'mm39,' 
            or 'dm6'

        tolerance : int
            Used for BLAT filtering. Number of acceptable matches 
            to other genomic loci. Default 25
    
        species : str
            DFAM species to check repeats, e.g. "Homo sapiens",
            "Mus musculus", or "Drosophila melanogaster"
    
    Returns
    _______
    
    output : a Pandas DataFrame
        A dataframe containing the final probes after filtering
        steps. Identical to the Probes.csv file
    
    rapProbesLog.out : a text file
        A text file containing a log of steps taken by the 
        rap_probes function
        
    [gene]_[probe_length]ntProbes.csv : a csv file
        A csv file containing the final probes. Identical
        to the Pandas Dataframe ouput
        
    blatFailedProbes.csv : a csv file
        If performing BLAT filtering, a csv file containing BLAT
        results for probes that did not pass filters
    
    blatPassedProbes.csv : a csv file
        If performing BLAT filtering, a csv file containing BLAT
        results for probes that passed filters
        
    dfamFailedProbes.csv : a csv file
        If performing Dfam filtering, a csv file containing Dfam
        results for probes that did not pass filters
    
    '''
    # Create directory to store results
    dirname = gene + '_rapProbesOutput'
    if os.path.exists(dirname):
        pass
    else:
        os.mkdir(dirname)
    
    # Create log file
    log = open(dirname + '/rapProbesLog.out','w')
    log.writelines('Probe Design Log for ' + gene + '\n')
    
    # Read file
    seq = seq_interpreter(fasta)

    # Remove polyA tail
    while seq[-1] == 'A':
        seq = seq[:-1]

    # Convert to sequence object
    seq = Seq(seq)
    
    # Extract indices of the desired probe length
    inds = np.arange(0, len(seq), probe_length-len(adaptseq))
    
    s_list = []
    
    for i in range(len(inds)-1):
        s_list.append(np.s_[inds[i]:inds[i+1]])
    
    # Use those indices to make probes
    s_seq = [seq[i] for i in s_list]
    
    # If there is more than a quarter probe of gene left uncovered, 
    # add one last probe 
    if len(seq) - inds[-1] > (probe_length-len(adaptseq)) / 4 : 
        s_seq.append(seq[-1*(probe_length-len(adaptseq)):])
    
    else:
        pass
    
    s_seq = [str(i.reverse_complement()) for i in s_seq]
    
    # Update log
    log.writelines('Original probes generated: ' + 
                   str(len(s_seq)) + '\n')
    
    # Filter with BLAT
    if blat == True:
        log.writelines('\n')
        print('Starting BLAT')
        keepdf, dropdf = blatfilt(seq,
                                 kwargs['genome'],
                                 s_seq,
                                 log=log,
                                 tolerance=25)
        
        # Export probes
        dropdf.to_csv(dirname + '/blatFailedProbes.csv',
                      index=False)
        keepdf.to_csv(dirname + '/blatPassedProbes.csv',
                      index=False)
        
        # Update seq list
        blatkeep = np.unique(keepdf['qName'])
        s_seq = [s_seq[int(i)] for i in blatkeep]
        
        # Update log
        log.writelines('Probes remaining after BLAT: ' + 
                       str(len(blatkeep)) + '\n')
        
        print('BLAT Done')
        
    else:
        pass
    
    # Filter with Dfam
    if dfam == True:
        log.writelines('\n')
        print('Starting Dfam')
        keep_probes, drop_probes = dfamfilt(s_seq, 
                                            kwargs['species'],
                                            dirname,
                                            log=log)
        
        # Update log
        log.writelines('Probes remaining after Dfam: ' + 
                      str(len(keep_probes)) + '\n')
        
        # Update seq list
        s_seq = [s_seq[int(i)] for i in keep_probes]
    
    else:
        pass
    
    # Close log
    log.close()
    
    # Generate final probe names
    prb_nms = [gene + '_' + str(i) for i in range(len(s_seq))]
            
    # Add adapt seq
    s_seq = [adaptseq + i for i in s_seq]
    
    # Add biotin
    if biotin == True:
        ['/5Biosg/' + i for i in s_seq]
        
    else:
        pass
    
    # Generate pandas dataframe and export to csv
    fname = gene + '_' + str(probe_length) + 'ntProbes.csv'
    fname = os.path.join(dirname,fname)
    
    df =  pd.DataFrame({'Name':prb_nms,
                        'Sequence':s_seq})
    
    df.to_csv(fname, index=False)
    
    print('Probe generation complete')
    
    return df
