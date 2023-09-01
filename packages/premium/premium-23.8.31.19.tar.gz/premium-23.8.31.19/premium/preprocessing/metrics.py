import unicodedata
from collections import defaultdict


def average_reports(reports, print=False):
    """try get average metrics from reports, which is a list of the following metrics
    {'B': {'precision': 0.7866666666666666, 'recall': 0.21223021582733814, 'f1-score': 0.3342776203966006, 'support': 278.0}, 'I': {'precision': 0.8365384615384616, 'recall': 0.21323529411764705, 'f1-score': 0.33984375, 'support': 408.0}, 'micro avg': {'precision': 0.8156424581005587, 'recall': 0.21282798833819241, 'f1-score': 0.3375722543352601, 'support': 686.0}, 'macro avg': {'precision': 0.8116025641025642, 'recall': 0.2127327549724926, 'f1-score': 0.3370606851983003, 'support': 686.0}, 'weighted avg': {'precision': 0.8163280257157808, 'recall': 0.21282798833819241, 'f1-score': 0.3375880881490597, 'support': 686.0}}
    """
    avg_reports = {}
    keys = []
    weights = {'micro avg': 9, 'macro avg': 10, 'weighted avg': 11}
    for r in reports:
        keys.extend(r.keys())
    keys = list(set(keys))
    keys.sort(key=lambda x: (weights.get(x, 0), x))

    for k in keys:
        dt = defaultdict(float)
        freq = defaultdict(int)
        for _report in reports:
            if k in _report:
                item = _report[k]
                for xk, v in item.items():
                    dt[xk] += v
                    freq[xk] += 1
        for xk, v in dt.items():
            dt[xk] = v / freq[xk]
            if xk == 'support':
                dt[xk] = int(dt[xk])
        avg_reports[k] = dict(dt)
    if print:
        format_print(avg_reports)
    return avg_reports


def format_print(report, digits=4):
    print('{:>15s} {:>10s} {:>10s} {:>10s} {:>10s}'.format(
        '', 'precision', 'recall', 'f1-score', 'support'))
    print()
    for k, v in report.items():
        if k == 'micro avg':
            print()

        # 针对全角字符，计算额外字符宽度
        extra_width = sum(
            unicodedata.east_asian_width(c) in ('F', 'W') for c in k)
        print(
            '{:>{padding}s} {:>10.{digits}f} {:>10.{digits}f} {:>10.{digits}f} {:>10d}'
            .format(k,
                    v['precision'],
                    v['recall'],
                    v['f1-score'],
                    v['support'],
                    padding=15 - extra_width,
                    digits=digits))
    print('-'*80)