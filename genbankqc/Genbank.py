import os
import traceback
import pandas as pd
from logbook import Logger

from genbankqc import Species


class Genbank:
    def __init__(self, path):

        """Genbank"""

        self.genbank = path
        self.path = path
        self.assembly_summary = os.path.join(
            self.genbank,
            ".info/assembly_summary.txt",
        )
        try:
            self.assembly_summary = pd.read_csv(
                self.assembly_summary,
                sep="\t",
                index_col=0,
            )
        except FileNotFoundError:
            pass
        self.log = Logger("init.genbank")
        self.log.info(self.genbank)


    @property
    def species(self):
        dirs = (
            os.path.join(self.genbank, d)
            for d in os.listdir(self.genbank)
            if os.path.isdir(d)
        )
        for d in dirs:
            fastas = len([f for f in os.listdir(d) if f.endswith('fasta')])
            if fastas > 5:
                try:
                    yield Species(d)
                except Exception:
                    print('Skipping ', d)
                    traceback.print_exc()
            else:
                print("Not enough fastas in {}".format(d))

    def qc(self):
        for i in self.species:
            try:
                i.qc()
            except Exception:
                print('Failed ', i.species)
                traceback.print_exc()
