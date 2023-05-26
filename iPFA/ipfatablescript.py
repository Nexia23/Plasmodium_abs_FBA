# cut ipfa table to relevant reactions
# add columns for substrate and product
# add column for Km and for Ki
# todo make general method for ['a', 'b', etc to a, b, etc
import pandas as pd
import numpy as np
from bioservices import KEGG
import urllib.request

subsystems = ['Fatty acid degradation', 'Glycerophospholipid metabolism',
              'Glycerolipid metabolism', 'Ether lipid metabolism', 'N-Glycan biosynthesis',
              'Lipoic acid metabolism', 'Phosphonate and phosphinate metabolism',
              'Sphingolipid metabolism', 'Fatty acid metabolism / biotin (vit B7) dependent',
              'Fatty acid metabolism', 'Isoprenoid metabolism', 'Steroid metabolism',
              'Glycosylphosphatidylinositol(GPI)-anchor biosynthesis']  # subsystems we want to consider


# todo: subsystems list not complete!

def formattoliststring(string):
    whitespacelist = string.split(' + ')
    nowhitespacelist = []
    for word in whitespacelist:
        y = word.strip()
        nowhitespacelist.append(y)
    nowhitespacelist = str(nowhitespacelist)
    nowhitespacelist = nowhitespacelist.replace('\'', '')
    nowhitespacelist = nowhitespacelist.replace('\"', '')
    nowhitespacelist = nowhitespacelist[1:-1]  # remove square brackets
    return nowhitespacelist  # which is now a list of stripped strings


# for a in table['SUBSTRATES']: #doesn't work, neither second nro 3rd work
#    a = str(a)
#    a = a[1:-1]
#    a.replace('\'', '')
# for b in table['PRODUCTS']:
#    b = b[1:-1]

def subsprodscols(table):
    substrates = []
    products = []

    for eq in table['EQUATION']:  # splitting equations into substrates and products
        streq = str(eq)
        subs, prods = streq.split(' <=> ')
        substrates.append(formattoliststring(subs))  # prints as x, y, z instead of ['x', 'y' etc
        products.append(formattoliststring(prods))

    return substrates, products


def newreactioncolumn(table):
    # make reaction names without compartment suffix
    reactions = []
    for r in table['ID']:  # works
        if len(r) != 8:
            reactions.append('not 1 reaction')
        else:
            reactions.append(r[:-2])
    return reactions


def compoundnumbers(columnname, keggobject):  # todo: remember already looked up and use, doesnt work w 2a -> B
    k = keggobject
    ccolumn = []  # this will be the masterlist that gets returned and then turned into a column
    counter = 0  # for seeing which row the error occurs in
    for row in table[columnname]:

        cnumbers = []  # this should be the list of compounds involved in each reaction
        for compound in row.split(', '):
            compound = compound[:-3]  # cut off compartment designation

            if compound[0] == 'G' and len(compound) == 6:  # meaning: if compound is a glycan id
                # todo: do we even want glycans?
                # uf = urllib.request.urlopen(f"http://rest.kegg.jp/get/{compound}")
                # html = uf.read()
                # html = html.decode('UTF-8')
                # words = html.split()
                # possibly use k.get('gl:{compound}'
                # if 10 < counter < 15:
                # print(f'the words is {words}')
                text = k.get(f'gl:{compound}')
                words = text.split()
                if 'as:' in words:
                    compoundid = words[words.index('as:') + 1]  # G00008 does not have compound id
                else:
                    cnumbers.append(compound)
                    continue
                cnumbers.append(compoundid)

            else:

                searchresult = k.find('compound', compound)  # if we have the english name

                assert searchresult != [''], f'Kegg search for {compound} returned empty '

                candidates = searchresult.split('\n')  # list of candidates
                while candidates[:-1] == '':
                    candidates = candidates[:-1]

                candidates2d = [candidate.split('\t') for candidate in candidates]

                for candidate in candidates2d:

                    candidate[0] = candidate[0][4:]
                    # print(candidate)
                    if not candidate[0]:  # deals with empty strings
                        continue

                    assert len(candidate) >= 2, f'candidate is weird, here is the candidate {candidate}'
                    candidate[1] = candidate[1].split(';')[0]

                    if candidate[1] == compound:
                        cnumbers.append(candidate[0])
                        break
        # print(cnumbers)
        ccolumn.append(cnumbers)
        print(f'counter is at {counter}')
        counter += 1
    return ccolumn


def formattonice(column):
    column2 = []
    for row in column:
        assert row, 'row is empty, last error was at counter 2:176'
        row = str(row)
        row = row.replace('\'', '')
        row = row.replace('\"', '')
        if row[0] == '[' and row[-1] == ']':
            row = row[1:-1]
        column2.append(row)
    column2 = pd.Series(column2)
    return column2


if __name__ == '__main__':
    table = pd.read_excel('ipfa_raven_input.xlsx', header=0)

    table = table.loc[:, 'ID':]
    table = table[table['SUBSYSTEM'].isin(subsystems)]  # first target achieved

    reactions = newreactioncolumn(table)
    substrates, products = subsprodscols(table)

    table['REACTIONID'] = reactions
    table['SUBSTRATES'] = substrates
    table['PRODUCTS'] = products

    k = KEGG()
    k.organism = 'pfa'

    table['CSUBSTRATE'] = formattonice(compoundnumbers('SUBSTRATES', k))
    table['CPRODUCT'] = formattonice(compoundnumbers('PRODUCTS', k))

    table['KM'] = np.nan
    table['isinhibited'] = np.nan
    table['KI'] = np.nan
    table['verified'] = np.nan
    #
    # table.to_csv('myipfaslice.csv')
    # table = pd.read_csv('myipfaslice.csv')
    #table['CSUBSTRATE'] = formattonice(table['CSUBSTRATE'])
    #table['CPRODUCT'] = formattonice(table['CPRODUCT'])
    table.to_csv('myipfaslice.csv')
