#Run the command line function in python
#Append dockerfile to have ./mmseqs

#Boilerplate
import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile

#Place all input file parameters into an ordered list that is fed to subprocess

@small_task
def search_task(fasta1: LatchFile, fasta2: LatchFile, output: str) -> LatchFile: 

    # A reference to our output. This needs to match exactly what MMSEQS easy-search would output
    tmp_output = Path(output).resolve()
    tmp_output.touch()

    #Exact command line args that would be used in terminal
    _easysearch_cmd = [
        "mmseqs",
        "easy-search",
        "--search-type",
        "3",
        "--remove-tmp-files",
        fasta1.local_path,
        fasta2.local_path,
        str(tmp_output),
        "tmp"
    ]

    subprocess.run(_easysearch_cmd)

    return LatchFile(str(tmp_output), "latch:///test.m8")

@workflow
def easy_search(fasta1: LatchFile, fasta2: LatchFile, output: str) -> LatchFile:
    """Description...

    markdown header
    ----

    Write some documentation about your workflow in
    markdown here:

    > Regular markdown constructs work as expected.

    # Heading

    * content1
    * content2

    __metadata__:
        display_name: Search for similar substrings between genomes, output m8 file of overlapping substrings.
        author:
            name:
            email:
            github:
        repository:
        license:
            id: MIT

    Args:

        fasta1:
          FASTA file 1 to be compared to FASTA file 2.

        fasta2:
          FASTA file 2 to be compared to FASTA file 1.

        latchoutput:
          Filename of the .m8 tmp output that will be produced


    """
    return search_task(fasta1=fasta1, fasta2=fasta2, output=output)