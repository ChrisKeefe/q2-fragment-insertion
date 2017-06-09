# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import shutil
import tempfile
import subprocess

from q2_types.feature_data import DNAFASTAFormat
from q2_types.tree import NewickFormat

from q2_fragment_insertion._format import PlacementsFormat


def _sanity():
    if shutil.which('java') is None:
        raise ValueError("java does not appear in $PATH")

    sepp = _sepp_path()
    if not os.path.exists(sepp):
        raise ValueError("Cannot find run-sepp.sh, expected it at: %s" % sepp)


def _sepp_path():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'assets/sepp-package/run-sepp.sh')


def _run(seqs_fp, threads, cwd):
    cmd = [_sepp_path(),
           seqs_fp,
           'q2-fragment-insertion',
           '-x', str(threads)]

    subprocess.run(cmd, check=True, cwd=cwd)


def sepp_16s_greengenes(representative_sequences: DNAFASTAFormat,
                        threads: int=1) -> (NewickFormat, PlacementsFormat):

    _sanity()

    placements = 'q2-fragment-insertion_placement.json'
    tree = 'q2-fragment-insertion_placement.tog.tre'

    placements_result = PlacementsFormat()
    tree_result = NewickFormat()

    with tempfile.TemporaryDirectory() as tmp:
        _run(str(representative_sequences), str(threads), tmp)
        outtree = os.path.join(tmp, tree)
        outplacements = os.path.join(tmp, placements)

        shutil.copyfile(outtree, str(tree_result))
        shutil.copyfile(outplacements, str(placements_result))

    return tree_result, placements_result
