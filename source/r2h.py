# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

class R2H(object):

    def __init__(self,chart):
        self.chart = ''
        with open(chart, encoding='utf-8') as chrt:
            for line in chrt:
                self.chart += line

    def chartParse(self):
        """
        @return chartDict
        ガ ==> g,a
        キ ==> k,i
        キャ ==> k,ya
        Similarily for Hiragana
        @setrofim : http://www.python-forum.org/pythonforum/viewtopic.php?f=3&t=31935
        """
        lines = self.chart.split('\n')
        chartDict = {}
        output = {}
        col_headings = lines.pop(0).split()
        for line in lines:
            cells = line.split()
            for i, c in enumerate(cells[1:]):
                output[c] = (cells[0], col_headings[i])
        for k in sorted(output.keys()):
            #@k = katakana
            #@r = first romaji in row
            #@c = concatinating romaji in column
            r, c = output[k]
            #k, r, c = [unicode(item,'utf-8') for item in [k,r,c]]
            if k == 'X':continue
            romaji = ''.join([item.replace('X', '') for item in [r,c]])
            chartDict[k] = romaji

        chartDict =  {v: k for k, v in chartDict.items()}

        self.chd = chartDict
        return chartDict

    def r2h(self,word):
        syllables = []
        while word:
            for n in reversed(range(1,4)):
                try:
                    syl = word[:n]
                    if syl in self.chd:
                        syllables.append(syl)
                        word = word[n:]
                except IndexError:
                    continue

        print(' '.join(syllables))
        return syllables

if __name__ == '__main__':
    r2h = R2H('hiraganaChart.txt')
    chd = r2h.chartParse()
    print(chd)
    r2h.r2h('tsudiko')
