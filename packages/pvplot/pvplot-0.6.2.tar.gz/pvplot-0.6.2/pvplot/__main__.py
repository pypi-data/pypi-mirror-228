#!/usr/bin/env python3
"""Dynamic plotting tool for control system frameworks.
Frameworks supported: EPICS, ADO, LiteServer.
The framework is distinguished by adding a prefix to Process Variable names:
'E:' - for EPICS, 'L:" - for LiteServer.
"""
import sys,os
from . import pvplot

def main():
    import argparse
    global pargs
    parser = argparse.ArgumentParser(description=__doc__
    ,formatter_class=argparse.ArgumentDefaultsHelpFormatter
    ,epilog=(f'pvplot: {pvplot.__version__}'))
    parser.add_argument('-a', '--ado', default='L:localhost:dev1', help=\
      'Default Device/ADO name. Useful for plotting parameters from single device.')
    parser.add_argument('-s', '--sleepTime', type=float, default=0.1,
      help='sleep time between data delivery [s]')
    parser.add_argument('-v', '--verbose', nargs='*', help=\
      'Show more log messages (-vv: show even more).')
    parser.add_argument('-x', '--xscale', help=\
     'Parameter, which provides dynamic scale for X-axis')
    parser.add_argument('-X', '--xrange', help=\
     'Fixed range of X axis, e.g: -x10:20')
    parser.add_argument('-y', '--yscale', help=\
     'Parameter, which provides dynamic scale for Y-axis')
    parser.add_argument('-Y', '--yrange', help=\
     'Fixed range of Y axis, e.g: -y1000:4095')
    parser.add_argument('-z', '--zoomin', type=float, default=1., help=\
      'Zoom the application window by a factor')
    parser.add_argument('-#','--dock', action='append', nargs='*', 
      help='''plot the ADO parameter in a specified dock, i.e: to plot the 
        scrolling plot in dock#1 and correlation plot in dock#2:
        -#0yMax  -#1yMin''')
    parser.add_argument('parms', nargs = '?', default='yMax yMin',
      help='''For stripchart: space-separated list, for correlation plot: comma-separated list of PVs.''')
    pargs = parser.parse_args()
    PVPlot = pvplot.PVPlot
    PVPlot.pargs = pargs
    print(f'pargs:{PVPlot.pargs}')
    if pargs.ado != '':
       pargs.ado += ':'

    #``````````````arrange keyboard interrupt to kill the program from terminal.
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
 
    PVPlot.start()

if __name__ == "__main__":
    main()
