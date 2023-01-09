#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 Virginia Tech.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
import logging
import numpy as np
from gnuradio import gr
import pmt
from time import time
#from fortress import rowbotreshape1, rowtopreshape1, columnfrontreshape1, columnbackreshape1, rowbotreshape2, rowtopreshape2, columnfrontreshape2, columnbackreshape2

###############################

#localsearch1
def rowtopreshape1(row, a):
    zerorow = a.shape[0]-a.shape[0]
    onerow = a.shape[0]- (a.shape[0]-1)
    lastrow = a.shape[0]-1
    secondtolastrow = a.shape[0]-2


    if row == zerorow:
        rowtop = row + 0
    elif row == onerow:
        rowtop = row - 0
    elif row ==lastrow:
        rowtop = row - 2
    elif row ==secondtolastrow:
        rowtop = row -1
    else:
        rowtop = row - 1
        
    return rowtop

def rowbotreshape1(row, a):
    zerorow = a.shape[0]-a.shape[0]
    onerow = a.shape[0]- (a.shape[0]-1)
    lastrow = a.shape[0]-1
    secondtolastrow = a.shape[0]-2

    if row == zerorow:
        rowbot = row + 3
    elif row == onerow:
         rowbot = row + 3
    elif row == lastrow:
         rowbot = row + 1
    elif row == secondtolastrow:
        rowbot = row + 2
    else:
        rowbot = row +2
    
    return rowbot

def columnfrontreshape1(column, a):
    zerocolumn = a.shape[1]-a.shape[1]
    onecolumn = a.shape[1]- (a.shape[1]-1)
    lastcolumn = a.shape[1]-1
    secondtolastcolumn = a.shape[1]-2

    if column == lastcolumn:
        columnfront = column - 2
    elif column == secondtolastcolumn:
        columnfront = column - 1
    elif column == onecolumn:
        columnfront = column - 1
    elif column == zerocolumn:
        columnfront = column + 0
    else:
        columnfront = column -1
        
    return columnfront

def columnbackreshape1(column, a):
    zerocolumn = a.shape[1]-a.shape[1]
    onecolumn = a.shape[1]- (a.shape[1]-1)
    lastcolumn = a.shape[1]-1
    secondtolastcolumn = a.shape[1]-2

    if column == lastcolumn:
        columnback = column + 1
    elif column == secondtolastcolumn:
        columnback = column + 2
    elif column == onecolumn:
        columnback = column + 2
    elif column == zerocolumn:
        columnback = column + 3
    else:
        columnback = column + 2

    return columnback

#25 beam wide search
def rowtopreshape2(row, a):
    zerorow = a.shape[0]-a.shape[0]
    onerow = a.shape[0]- (a.shape[0]-1)
    lastrow = a.shape[0]-1
    secondtolastrow = a.shape[0]-2


    if row == zerorow:
        rowtop = row + 0
    elif row == onerow:
        rowtop = row - 1
    elif row ==lastrow:
        rowtop = row - 4
    elif row ==secondtolastrow:
        rowtop = row -3
    else:
        rowtop = row - 2
        
    return rowtop

def rowbotreshape2(row, a):
    zerorow = a.shape[0]-a.shape[0]
    onerow = a.shape[0]- (a.shape[0]-1)
    lastrow = a.shape[0]-1
    secondtolastrow = a.shape[0]-2

    if row == zerorow:
        rowbot = row + 5
    elif row == onerow:
         rowbot = row + 4
    elif row == lastrow:
         rowbot = row + 1
    elif row == secondtolastrow:
        rowbot = row + 2
    else:
        rowbot = row +3
    
    return rowbot

def columnfrontreshape2(column, a):
    zerocolumn = a.shape[1]-a.shape[1]
    onecolumn = a.shape[1]- (a.shape[1]-1)
    lastcolumn = a.shape[1]-1
    secondtolastcolumn = a.shape[1]-2

    if column == lastcolumn:
        columnfront = column - 4
    elif column == secondtolastcolumn:
        columnfront = column - 3
    elif column == onecolumn:
        columnfront = column - 1
    elif column == zerocolumn:
        columnfront = column + 0
    else:
        columnfront = column -2
        
    return columnfront

def columnbackreshape2(column, a):
    zerocolumn = a.shape[1]-a.shape[1]
    onecolumn = a.shape[1]- (a.shape[1]-1)
    lastcolumn = a.shape[1]-1
    secondtolastcolumn = a.shape[1]-2

    if column == lastcolumn:
        columnback = column + 1
    elif column == secondtolastcolumn:
        columnback = column + 2
    elif column == onecolumn:
        columnback = column + 4
    elif column == zerocolumn:
        columnback = column + 5
    else:
        columnback = column + 3

    return columnback

###########################################3

class beam_selector(gr.basic_block):
    """
    Method that selects the best beam for IA
    """
    def __init__(self,
             pair_file="/home/adrian/sel_pair.log",
             kpi_file="/home/adrian/sel_kpi.log",
             threshold=0.0,
             debug=False,
        ):

        #self.logging.info(f'LOGLOGLOGLOGLOGLOGLOGLOGLOGLOG\n\n\n\n\n')

        self.pattern = np.arange(63)
        self.pattern.shape = (7,9)
        # Check if the threshold is not a positiver number
        if threshold < 0.0:
            raise ValueError("Negative threshold:" + str(threshold) )

        gr.basic_block.__init__(self,
            name="Beam Selector",
            in_sig=None,
            out_sig=None)

        # Save parameters as class variables
        self._threshold = threshold

        logging.basicConfig(
            level=logging.DEBUG if debug else logging.INFO,
            format='[%(levelname)s] [%(name)s] %(message)s'
        )
        self.logging = logging.getLogger(self.name())

        self._sel_counter = 0
        self._kpi_counter = 0
        self._beam_store = {}

        # Register message port
        self.message_port_register_in(pmt.intern('trigger'))
        self.message_port_register_in(pmt.intern('kpi_in'))
        self.message_port_register_out(pmt.intern('sweep'))


        # Assign sweep CTL message handler
        self.set_msg_handler(pmt.intern('trigger'), self.trigger_msg_handler)
        self.set_msg_handler(pmt.intern('kpi_in'), self.val_msg_handler)

        # Open file and add headers
        self.results = open(pair_file, "w")
        self.results.write("#,TX,RX,KPI,elapsed\n")

        self.kpi = open(kpi_file, "w")
        self.kpi.write("#,TX,RX,KPI\n")

    def stop(self):
        """
        Called at the end of the flowgraph execution to free resources
        """
        self.results.close()
        self.kpi .close()

        return gr.basic_block.stop(self)


    def val_msg_handler(self, msg):
        # Convert message to python
        p_msg = pmt.to_python(msg)
        # Print debug information
        self.logging.debug(f'Received Value message: {p_msg}')

        # Check if we receive a new sweep state
        kpi = p_msg.get('val', -999.0)
        # Check if we receive  a beam ID for the TX
        tx_beam = p_msg.get('tx', 32)
        # Check if we receive  a beam ID for the RX
        rx_beam = p_msg.get('rx', 32)

        # Check if we need to create a new entry in the beam store
        if (tx_beam, rx_beam) not in self._beam_store:
            self._beam_store[(tx_beam, rx_beam)] = []

        if self.trigger:
            self._beam_store[(tx_beam, rx_beam)].append(kpi)

        self._kpi_counter += 1
        self.kpi.write(f"{self._kpi_counter},{tx_beam},{rx_beam},{kpi}\n")

    def trigger_msg_handler(self, msg):
        # Convert message to python
        p_msg = pmt.to_python(msg)
        # Print debug information
        self.logging.debug(f'Received trigger message: {p_msg}')

        # Check if we receive a new sweep state
        if 'trigger' not in p_msg:
            # Raise error
            raise ValueError('Missing references to a trigger: ' + str(p_msg))

        # Set the new valuep
        self.trigger = p_msg.get('trigger', True)


        # When triggered, reset saved information
        if self.trigger:
            self._sel_counter += 1
            self._beam_store = {}

        else:
            start = time()
            # Get the average KPI values per beam pair
            for beam_pair in self._beam_store:
                self._beam_store[beam_pair] = np.median(self._beam_store[beam_pair])

            if self._beam_store:
                # Extract the beam pair with highest KPI
                tx_beam, rx_beam = max(self._beam_store, key=self._beam_store.get)
                kpi = self._beam_store[(tx_beam, rx_beam)]


                if self._sel_counter >=1:
                    txnrow, txncol = self.pattern.shape
                    txMax = tx_beam
                    TXrid = txMax//txncol 
                    TXcid = txMax%txncol
                    (TXrid, TXcid)
                    TXrow = TXrid
                    TXcolumn = TXrid
                    TXrowtop = rowtopreshape2(TXrow, self.pattern)
                    TXrowbot = rowbotreshape2(TXrow, self.pattern)
                    TXcolfront = columnfrontreshape2(TXcolumn, self.pattern)
                    TXcolback = columnbackreshape2(TXcolumn, self.pattern)
                    tx = self.pattern[TXrowtop:TXrowbot, TXcolfront:TXcolback]
                    #tx = btx.flatten

                    rxnrow, rxncol = self.pattern.shape
                    RxMax = rx_beam
                    RXrid = RxMax//rxncol 
                    RXcid = RxMax%rxncol
                    (RXrid, RXcid)
                    RXrow = RXrid
                    RXcolumn = RXrid
                    RXrowtop = rowtopreshape2(RXrow, self.pattern)
                    RXrowbot = rowbotreshape2(RXrow, self.pattern)
                    RXcolfront = columnfrontreshape2(RXcolumn, self.pattern)
                    RXcolback = columnbackreshape2(RXcolumn, self.pattern)
                    rx = self.pattern[RXrowtop:RXrowbot, RXcolfront:RXcolback]
                    #rx = brx.flatten()
                
                else:
                    tx = self.pattern
                    #tx = btx.flatten()
                    rx = self.pattern
                    #rx = brx.flatten()


            # Measure elapsed time
            elapsed = time() - start

            if self._beam_store:
                # Report findings
                self.logging.info(f'ADRIAN Pair TX {tx_beam} RX {rx_beam} RSS {kpi} Time {elapsed}')
                self.logging.info(f'Pattern TX {tx} RX {rx}')
                self.logging.info(f'ADRIANSADRIANSADRIANSbeampair RX {rx} TX {tx}')

                # Use the best beam
                self.message_port_pub(
                    pmt.intern('sweep'),
                    pmt.to_pmt({"set_beam":{'tx': tx_beam, 'rx': rx_beam}, "set_pattern": {'TX':tx.flatten().tolist(), 'RX': rx.flatten().tolist()}})
                    #.flatten()).tolist())
                )
                self.results.write(f"{self._sel_counter},{tx_beam},{rx_beam},{tx},{rx},{kpi},{elapsed}\n")

            else:
                # Report findings
                self.logging.info(f'Failed IA, could find find a beam pair')

                # Use the best beam
                self.message_port_pub(
                    pmt.intern('sweep'),
                    pmt.to_pmt({"set_beam": {'tx': 0, 'rx': 0}, "set_pattern": {'TX':[], 'RX': []}})
                )
                self.results.write(f"{self._sel_counter},0,0,0,{elapsed}\n")
