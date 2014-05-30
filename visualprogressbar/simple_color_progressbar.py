"""A simple CSS progress bar to be rendered in the IPython Notebook.
"""
#-----------------------------------------------------------------------------
# Authors: Ruaridh Thomson <echelous@me.com>
# License: MIT License
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import uuid
import struct

import seaborn as sns
from IPython.display import HTML, Javascript, display

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

HTML_TEMPLATE = """
<style>
  /*
   * Copyright (c) 2012-2013 Thibaut Courouble
   * http://www.cssflow.com
   *
   * Licensed under the MIT License:
   * http://www.opensource.org/licenses/mit-license.php
   *
   * View the Sass/SCSS source at:
   * http://www.cssflow.com/snippets/animated-progress-bar/demo/scss
   *
   * Original PSD by Vin Thomas: http://goo.gl/n1M2e
   */
  .contanya {
    margin: 10px auto;
    width: auto;
    text-align: center;
  }

  .contanya .progress-%s {
    margin: 0 5% auto;
    width: auto;
  }

  .progress-%s {
    padding: 4px;
    background: rgba(0, 0, 0, 0.25);
    color: rgba(0, 0, 0, 0.5);
    border-radius: 6px;
    -webkit-box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.25), 0 1px rgba(255, 255, 255, 0.08);
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.25), 0 1px rgba(255, 255, 255, 0.08);
  }

  .progress-bar-%s {
    height: 16px;
    border-radius: 4px;
    background-image: -webkit-linear-gradient(top, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.05));
    background-image: -moz-linear-gradient(top, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.05));
    background-image: -o-linear-gradient(top, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.05));
    background-image: linear-gradient(to bottom, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.05));
    -webkit-transition: 0.4s linear;
    -moz-transition: 0.4s linear;
    -o-transition: 0.4s linear;
    transition: 0.4s linear;
    -webkit-transition-property: width, background-color;
    -moz-transition-property: width, background-color;
    -o-transition-property: width, background-color;
    transition-property: width, background-color;
    -webkit-box-shadow: 0 0 1px 1px rgba(0, 0, 0, 0.25), inset 0 1px rgba(255, 255, 255, 0.1);
    box-shadow: 0 0 1px 1px rgba(0, 0, 0, 0.25), inset 0 1px rgba(255, 255, 255, 0.1);
  }

  .progress-%s > .progress-bar-%s {
    width: 10%;
    background-color: #fee493;
  }
  </style>
  <div class="contanya">
    <div class="progress-%s">
      <div id="progress-bar-%s" class="progress-bar-%s"></div>
    </div>
  </div>
"""

#-----------------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------------

class SimpleColorProgressBar(object):
    """ SimpleColorBar creates and renders a simple, yet pretty, progress bar
    that is easy to use.

    Parameters
    ----------
    color_palette : String
        Name of the color palette to be used for the bar. Any palette available
        in Seaborn or matplotlib can be used.
    num_iterations : int
        The number of iterations that the progressbar is tracking.

    Examples
    --------
    >>> pb = SimpleColorProgressBar(color_palette='winter', num_iterations=100)
    >>> for i in range(100):
    ...     time.sleep(0.1)
    ...     pb.update()
    """
    def __init__(self, color_palette='RdYlGn', num_iterations=100):
        self.colors = get_colour_palette(name=color_palette)
        self.num_iterations = num_iterations
        self.update_weight = 100.0 / num_iterations
        self.loop_count = 0
        self.prev_update_count = 0

        self._setup_progress_bar()

    def _setup_progress_bar(self):
        """
        Setup the HTML, CSS and JS content of the progress bar and display it in
        the notebook.
        """
        self.divid = str(uuid.uuid4())

        html_body = HTML_TEMPLATE.replace('%s', self.divid)

        pb = HTML(html_body)
        display(pb)

    def _get_color_palette(self, name='RdYlGn', n_colors=100):
        """
        A bit of information telling us what this function does. Example
        parameter and return decriptions below.

        Parameters
        ----------
        name : String, default 'RdYlGn'
            Name of the color palette to be loaded.
        n_colors : int, default 100
            Number of colours to be loaded into the palette.

        Returns
        -------
        palette_strings : list
        """
        palette = sns.color_palette(name=name, n_colors=n_colors)

        palette_strings = []

        for r, g, b in palette:
            r_val = r * 255.0
            g_val = g * 255.0
            b_val = b * 255.0

            colour_string = struct.pack('BBB', r_val,
                                        g_val, b_val).encode('hex')

            palette_strings.append(colour_string)

        return palette_strings

    def update(self):
        """
        Update the progress bar, taking into account the current loop count.
        """
        update_count = int(self.loop_count * self.update_weight)

        if self.loop_count == self.num_iterations-1:
            update_count = 99

        self.loop_count += 1

        #update_string = str(update_count) + ' / ' + str(self.num_iterations)

        js_string = """
        var progbar = document.querySelector(".progress-%s > .progress-bar-%s");

        progbar.style.width = "%i%%";
        progbar.style.backgroundColor = "#%s";
        """ % (self.divid, self.divid, update_count+1,
               self.colors[update_count])

        if update_count > self.prev_update_count:
            display(Javascript(js_string))

        self.prev_update_count = update_count
