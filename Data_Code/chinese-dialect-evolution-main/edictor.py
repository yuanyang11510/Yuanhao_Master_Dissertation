from pyedictor import fetch
import lingpy
from lingpy import *
from collections import defaultdict
from tabulate import tabulate
from skbio.stats.distance import mantel

wl = fetch("liusinitic", remote_dbase="liusinitic2.sqlite3", to_lingpy=True)
wl.output('tsv', filename="liusinitic", ignore="all", prettify=False)
#wl = Wordlist("liusinitic.tsv")

ignored_concepts = [
        "wife",
        "husband",
        "father",
        "child",
        "mather[sic]",
        "man",
        "woman",
        "what",
        "they",
        "we",
        "dirty",
        "how",
        "this",
        "here",
        "give",
        "mather",
        "where",
        "that",
        "there",
        ]


# check data
table = []
ignore = []
for idx in wl:
    wy = wl[idx, "wenyan"].split("+")
    tks = wl[idx, "tokens"]
    cogids = wl[idx, "cogids"]
    if len(wy) != len(tks.n) or len(wy) != len(cogids) or len(wy) != len(wl[idx, "morphemes"]):
        table += [[str(idx), wl[idx, "concept"], wl[idx, "doculect"], " ".join(wy), tks, 
                   basictypes.ints(cogids), basictypes.strings(wl[idx,
                                                                  "morphemes"])]]
        ignore += [idx]
    wl[idx, "wenyan"] = basictypes.strings(wy)
print(tabulate(table, tablefmt="pipe", headers=["ID", "Concept", "Doculect",
                                                "Wneyan", "Tokens", "Cogids",
                                                "Morphemes"]))

B, C = {}, {}
etd = wl.get_etymdict(ref="cogids")
max_cog = max(etd) + 1
for idx, concept, doculect, subgroup, cogids, wenyan in wl.iter_rows(
        "concept", "doculect", "subgroup", "cogids", "wenyan"):
    if idx not in ignore:
        # borrowing if MIN and 3 or 2
        new_cogids, new_wenyan = [], []
        for cogid, wy in zip(cogids, wenyan):
            if cogid == 0:
                pass
            else:
                new_cogids += [cogid]
                new_wenyan += [wenyan]
        # non-borrowed part
        C[idx] = "-".join([concept, "-".join([str(cogid) for cogid in
                                             new_cogids])])
        # borrowed if Min and 3 or 2
        if (subgroup == "Min" and "3" in wenyan) or (subgroup == "Min" and "2"
                                                     in wenyan):
            B[idx] = concept + "-" + str(max_cog)
            max_cog += 1
        elif subgroup != "Min" and "1" in wenyan:
            B[idx] = concept + "-" + str(max_cog)
            max_cog += 1
        elif "3" in wenyan:
            B[idx] = concept + "-" + str(max_cog)
            max_cog += 1
        else:
            B[idx] = "-".join([concept, "-".join([str(cogid) for cogid in
                                             new_cogids])])
    else:
        C[idx] = max_cog
        B[idx] = max_cog
        max_cog += 1

            
wl.add_entries("nobor", C, lambda x: x)
wl.renumber("nobor")
wl.add_entries("bor", B, lambda x: x)
wl.renumber('bor')

new_wl1 = {0: wl.columns}
new_wl2 = {0: wl.columns}
for idx in wl:
    if idx not in ignore and wl[idx, "concept"] not in ignored_concepts:
        new_wl1[idx] = wl[idx]
        new_wl2[idx] = wl[idx]

new_wl1 = Wordlist(new_wl1)
new_wl2 = Wordlist(new_wl2)
treeA = new_wl1.calculate("tree", ref="noborid")
treeB = new_wl2.calculate("tree", ref="borid")
new_wl1.calculate('dst', ref="noborid")
new_wl2.calculate('dst', ref='borid')
new_wl1.output('dst', filename="distances-no-borrowing")
new_wl2.output('dst', filename="distances-yo-borrowing")

new_wl1.output("tsv", filename="wordlist-no-borrowing", ignore="all",
               prettify=False,
               subset=True,
               cols=["doculect", "concept", "value", "tokens",
                        "cogids",
                        "noborid"])
new_wl2.output("tsv", filename="wordlist-with-borrowing", ignore="all",
               prettify=False,
               subset=True,
               cols=["doculect", "concept", "value", "tokens",
                        "cogids",
                        "borid"])


coeff, p_value, _ = mantel(new_wl1.distances, new_wl2.distances)
print(coeff, p_value)
