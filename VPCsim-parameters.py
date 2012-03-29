"""
 * Copyright (c) Contributors http://github.com/aduffy70/VPCsim-parameters
 * See CONTRIBUTORS.TXT for a full list of copyright holders.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the VPCsim-parameters module nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE DEVELOPERS ``AS IS'' AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE CONTRIBUTORS BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import time


class HtmlPage():
    """
    Class containing basic html page layout.
    """
    header = '<html><head><title>%s</title></head><body>'

    instructions = """
        <p>
            This form generates virtual plants in a simulated plant community growing
            in the 3D virtual space. Changes made here will not take effect until
            they are enabled there.<br>
        </p>
        <hr>
        """

    footer = '</body></html>'


class MeadowRecordObject(db.Model):
    """
    Record class representing all the parameters to run a community simulation.
    """
    # Timestamp id for this record
    id = db.StringProperty()

    # CSV integers represeting the Unity3D Tree types for each of the 5 species in the community
    plant_types = db.StringProperty()

    #Water, light, temperature, and disturbance levels
    water_level = db.IntegerProperty()
    light_level = db.IntegerProperty()
    temperature_level = db.IntegerProperty()
    disturbance_level = db.IntegerProperty()

    #Matrix representing the starting values for each position in the matrix
    #(R=random, N=disturbance, 0=gap, 1-5=plant types)
    starting_matrix = db.TextProperty()


class ParametersFormPageOne(webapp.RequestHandler):
    """
    First page of the three page community parameters form.
    Accessed by the user by url or hyperlink. Controls terrain
    and environment parameters (and includes some hidden matrix parameters).
    """
    def get(self):
        page = HtmlPage()
        self.response.out.write(page.header % 'Simulation parameters form')
        self.response.out.write(page.instructions)
        self.response.out.write(self.form)
        self.response.out.write(page.footer)

    form = """
        <form enctype="multipart/form-data" action="/parametersform2" method="post">
            <p>
                <b>Select the water/moisture/precipitation level:</b><br>
                <input type="radio" name="water_level" value="4">Highest<br>
                <input type="radio" name="water_level" value="3">Higher<br>
                <input type="radio" name="water_level" value="2" checked>Normal<br>
                <input type="radio" name="water_level" value="1">Lower<br>
                <input type="radio" name="water_level" value="0">Lowest<br>
            </p>
            <p>
                <b>Select the light level:</b><br>
                <input type="radio" name="light_level" value="4">Highest<br>
                <input type="radio" name="light_level" value="3">Higher<br>
                <input type="radio" name="light_level" value="2" checked>Normal<br>
                <input type="radio" name="light_level" value="1">Lower<br>
                <input type="radio" name="light_level" value="0">Lowest<br>
            </p>
            <p>
                <b>Select the temperature level:</b><br>
                <input type="radio" name="temperature_level" value="4">Highest<br>
                <input type="radio" name="temperature_level" value="3">Higher<br>
                <input type="radio" name="temperature_level" value="2" checked>Normal<br>
                <input type="radio" name="temperature_level" value="1">Lower<br>
                <input type="radio" name="temperature_level" value="0">Lowest<br>
            </p>
            <input type="submit" value="Continue...">
        </form>
        """


class ParametersFormPageTwo(webapp.RequestHandler):
    """
    Second page of the three page community parameters form.
    Accessed by the user by submitting ParametersFormPageOne.
    Controls plant settings
    """
    def post(self):
        page = HtmlPage()
        self.response.out.write(page.header % 'Simulation parameters form')
        self.response.out.write(self.form_header)
        for i in range(1,6):
            default_selection = ['', '', '', '', '']
            default_selection[i - 1] = 'selected="selected"'
            link_option = ''
            none_option = self.form_none_option
            if (i == 1):
                link_option = self.form_plant_examples_link
                none_option = ''
            self.response.out.write(self.form_plant_data %
                                    (i, i, none_option,
                                     default_selection[0], default_selection[1],
                                     default_selection[2], default_selection[3],
                                     default_selection[4], link_option))
        self.response.out.write(self.form_hidden_fields %
                                (self.request.get('water_level'),
                                 self.request.get('light_level'),
                                 self.request.get('temperature_level')))
        self.response.out.write(self.form_submit_button)
        self.response.out.write(page.footer)

    form_header = """
        <form enctype="multipart/form-data" action="/parametersform3" method="post">
        <p>
            <b>Select 5 plant species to include in the community:</b>
        </p>
        """

    form_plant_data = """
        <p>
            &nbsp;&nbsp;Species %s
            <select name="plant_code_%s">
                %s
                <option value = "0">Alder</option>
                <option value = "1" %s>Aspen</option>
                <option value = "2">Starthistle</option>
                <option value = "3">Juniper</option>
                <option value = "4">Serviceberry</option>
                <option value = "5">Sagebrush</option>
                <option value = "6">Sumac</option>
                <option value = "7">Wildrose</option>
                <option value = "8" %s>Fern</option>
                <option value = "9" %s>Maple</option>
                <option value = "10">Elderberry</option>
                <option value = "11" %s>Pine</option>
                <option value = "12">Cottonwood</option>
                <option value = "13" %s>Willow</option>
            </select>
            %s
        """

    form_none_option = """<option value = "-1">**None**</option>"""

    form_plant_examples_link = '<a href="/plants" target="_blank">View examples</a>'

    form_hidden_fields = """
        <input type="hidden" name="water_level" value="%s">
        <input type="hidden" name="light_level" value="%s">
        <input type="hidden" name="temperature_level" value="%s">
        """

    form_submit_button = '</p><input type="submit" name="next" value="Continue..."></form>'


class GetParameters(webapp.RequestHandler):
    """
    Returns the community record with a particular timestamp as XML.
    Accessed by the vMeadow opensim module.
    """
    def get(self):
        data = db.GqlQuery("SELECT * FROM MeadowRecordObject WHERE id=:1",
                            self.request.get('id'))
        if (data.count() == 1):
            #if there are no records or more than one, something has gone wrong and
            #we are better off NOT sending anything.
            self.response.out.write(data[0].to_xml())


class PlantPicturesPage(webapp.RequestHandler):
    """
    Displays a page with photos of the different plant types in a new browser window.
    Accessed through links on the SetupMatrix page form.
    """
    def get(self):
        page = HtmlPage()
        self.response.out.write(page.header % 'Species info')
        for i in range(14):
            self.response.out.write(self.plant_info_display % (self.common_names[i],
                                    self.latin_binomials[i],
                                    self.common_names[i],
                                    self.lifespans[i],
                                    self.water_levels[i],
                                    self.light_levels[i],
                                    self.temperature_levels[i],
                                    self.altitudes[i],
                                    self.colonizing_levels[i],
                                    self.replaces_lists[i],
                                    self.replaced_by_lists[i],
                                    self.other_notes[i]))
        self.response.out.write(page.footer)

    plant_info_display = """
        <p>
            <big><b>%s</b></big> (<i>%s</i>)
            <table border="0"><tbody><tr valign="top">
                <td>
                    <img src="/images/%s.png" height="250" width="300"/>
                </td>
                <td>
                    <b>Lifespan:</b> %s<br><br>
                    <b>Water:</b> %s<br>
                    <b>Light:</b> %s<br>
                    <b>Temp:</b> %s<br>
                    <b>Altitude:</b> %s<br><br>
                    <b>Colonizer:</b> %s<br>
                    <b>Outcompetes:</b> %s<br>
                    <b>Outcompeted by:</b> %s<br><br>
                    <b>Other notes:</b> %s
                </td>
            </tr></tbody></table>
        </p>
        """

    common_names = ['Alder',
                    'Aspen',
                    'Starthistle',
                    'Juniper',
                    'Serviceberry',
                    'Sagebrush',
                    'Sumac',
                    'Wildrose',
                    'Fern',
                    'Maple',
                    'Elderberry',
                    'Pine',
                    'Cottonwood',
                    'Willow']

    latin_binomials = [ 'Alnus tenuifolia',
                        'Populus tremuloides',
                        'Centaurea solstitialis',
                        'Juniperus scopulorum',
                        'Amelanchier utahensis',
                        'Artemesia tridentata',
                        'Rhus glabra',
                        'Rosa woodsii',
                        'Pteridium aquilinum',
                        'Acer grandidentatum',
                        'Sambucus nigra',
                        'Pinus ponderosa',
                        'Populus trichocarpa',
                        'Salix fragilis']

    water_levels = ['N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'H',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N']

    light_levels = ['N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N']

    temperature_levels = ['N',
                          'N',
                          'N',
                          'N',
                          'N',
                          'N',
                          'N',
                          'N',
                          'N',
                          'N',
                          'N',
                          'N',
                          'N',
                          'N']

    altitudes = [   'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N',
                    'N']

    lifespans = [   'M',
                    'M',
                    'M',
                    'M',
                    'M',
                    'M',
                    'M',
                    'M',
                    'M',
                    'M',
                    'M',
                    'M',
                    'M',
                    'M']

    colonizing_levels = [   'N',
                            'N',
                            'Y',
                            'N',
                            'N',
                            'N',
                            'N',
                            'N',
                            'N',
                            'N',
                            'N',
                            'N',
                            'N',
                            'N']

    replaces_lists = [  'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants',
                        'A, list, of, plants']

    replaced_by_lists = ['A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants',
                         'A, list, of, plants']

    other_notes = [ 'Some, relevant, facts',
                    'Some, relevant, facts',
                    'Invasive species',
                    'Some, relevant, facts',
                    'Some, relevant, facts',
                    'Some, relevant, facts',
                    'Some, relevant, facts',
                    'Some, relevant, facts',
                    'Some, relevant, facts',
                    'Some, relevant, facts',
                    'Some, relevant, facts',
                    'Some, relevant, facts',
                    'Some, relevant, facts',
                    'Some, relevant, facts']


class ParametersFormPageThree(webapp.RequestHandler):
    """
    Page 3 of the three page parameters request form.
    Accessed by submitting ParametersFormPageTwo.
    Controls starting matrix and disturbance settings and stores the
    output from all three pages.
    """
    def post(self):
        submit_value = self.request.get('submit_value')
        if (submit_value == 'Submit parameters'):
            page = HtmlPage()
            self.response.out.write(page.header % 'Simulation parameters form')
            self.id = str(int(time.time() * 1000.0))
            self.store_record()
            self.response.out.write(self.success_output_all_parameters % self.id)
            self.response.out.write(page.footer)
        else:
            self.redraw_form(submit_value)

    def redraw_form(self, submit_value):
        page = HtmlPage()
        disturbance_level = self.request.get('disturbance_level')
        starting_matrix = list(self.request.get('starting_matrix'))
        if (len(starting_matrix) == 0):
            #Set up the default starting matrix with all Rs
            starting_matrix = []
            for i in range(2500):
                starting_matrix.append('R')
        clicked = ''
        if ((submit_value == '') and (self.request.get('next') == '')):
            argument_list = self.request.arguments()
            argument_list.sort()
            submit_value = argument_list[0].split('.')[0][3:]
            clicked = submit_value
        selected = []
        selected_string = self.request.get('selected')
        if (selected_string != ''):
            selected = selected_string.split(',')
        if (submit_value == 'Apply cell value to cells'):
            cell_value = self.request.get('cell_value')
            for cell in selected:
                starting_matrix[int(cell)] = cell_value
            selected = []
        elif (submit_value == 'Apply cell value to area'):
            cell_value = self.request.get('cell_value')
            selected_area = self.get_area_list_from_corners(int(selected[0]), int(selected[1]))
            for cell in selected_area:
                starting_matrix[int(cell)] = cell_value
            selected = []
        elif (submit_value in selected):
            selected.remove(submit_value)
        else:
            selected.append(clicked)
        self.response.out.write(page.header % 'Simulation parameters form')
        self.response.out.write(self.form_header)
        if (disturbance_level == '1'):
            self.response.out.write(self.form_ongoing_disturbance_selector % (
            '', 'selected', '', '', ''))
        elif (disturbance_level == '2'):
            self.response.out.write(self.form_ongoing_disturbance_selector % (
            '', '', 'selected', '', ''))
        elif (disturbance_level == '3'):
            self.response.out.write(self.form_ongoing_disturbance_selector % (
            '', '', '', 'selected', ''))
        elif (disturbance_level == '4'):
            self.response.out.write(self.form_ongoing_disturbance_selector % (
            '', '', '', '', 'selected'))
        else:
            self.response.out.write(self.form_ongoing_disturbance_selector % (
            'selected', '', '', '', ''))
        self.response.out.write(self.form_starting_matrix_map_label)
        self.response.out.write(self.form_table_header)
        for j in range(50):
            for i in range(50):
                index = (j * 50) + i
                if (str(index) in selected):
                    image = 'selected'
                else:
                    image = starting_matrix[index]
                self.response.out.write(self.form_button % (index, image))
            if (j != 49):
                self.response.out.write('<br>')
        self.response.out.write(self.form_table_footer)
        if (len(selected) > 0):
            plant_codes_list = []
            for i in range(1,6):
                plant_code = self.request.get('plant_code_%s' % i)
                if (plant_code != '-1'):
                    plant_codes_list.append(plant_code)
            plant_codes_count = len(plant_codes_list)
            self.response.out.write(self.form_cell_value_selector_header)
            for i in range(0,plant_codes_count):
                self.response.out.write(self.form_cell_value_selector_option %
                                        (i+1, self.common_names[int(plant_codes_list[i])]))
            self.response.out.write(self.form_cell_value_selector_footer)
            self.response.out.write(self.form_assign_cells_button)
            if (len(selected) == 2):
                self.response.out.write(self.form_assign_area_button)
        else:
            self.response.out.write('<br>')
        self.response.out.write(self.form_submit_button)
        #Pass the list of selected cells, the current starting matrix, and ongoing disturbance value.
        self.response.out.write(self.form_active_hidden_fields % (
            ','.join(selected),''.join(starting_matrix)))
        #Pass the values from previous form pages
        self.response.out.write(self.form_passive_hidden_fields % (
            self.request.get('water_level'),
            self.request.get('light_level'),
            self.request.get('temperature_level')))
        for x in range(1, 6):
            self.response.out.write(self.form_plant_code_hidden_field %
                                    (x, self.request.get('plant_code_%s' % x)))
        self.response.out.write(self.form_footer)
        self.response.out.write(page.footer)

    def get_area_list_from_corners(self, corner1, corner2):
        y1 = corner1 / 50
        x1 = corner1 % 50
        y2 = corner2 / 50
        x2 = corner2 % 50
        lower_x = x1
        upper_x = x2
        lower_y = y1
        upper_y = y2
        if (x1 >= x2):
            lower_x = x2
            upper_x = x1
        if (y1 >= y2):
            lower_y = y2
            upper_y = y1
        area_list = []
        for y in range(lower_y, upper_y + 1):
            for x in range(lower_x, upper_x + 1):
                area_list.append(y * 50 + x)
        return area_list

    def store_record(self):
        # Get a db record instance to hold the form data
        record = MeadowRecordObject()
        # Store a timestamp as the record id
        record.id = self.id
        # Store the water_level, light_level, and temperature_level, and list of plant_species.
        record.water_level = int(self.request.get('water_level'))
        record.light_level = int(self.request.get('light_level'))
        record.temperature_level = int(self.request.get('temperature_level'))
        plant_codes_list = []
        for i in range(1,6):
            plant_code = self.request.get('plant_code_%s' % i)
            if (plant_code != '-1'):
                plant_codes_list.append(plant_code)
        record.plant_types = ''
        if (len(plant_codes_list) != 0):
            record.plant_types = ','.join(plant_codes_list)
        record.disturbance_level = int(self.request.get('disturbance_level'))
        # Store the community matrix
        #This matrix starts with 0 in the NW corner and I need 0 in the SW corner
        temp_starting_matrix = self.request.get('starting_matrix')
        upside_down_matrix = []
        for y in range(50):
            row = ''
            for x in range(50):
                row += temp_starting_matrix[y * 50 + x]
            upside_down_matrix.append(row)
        record.starting_matrix = ''
        for y in range(50):
            record.starting_matrix += upside_down_matrix[49 - y]
        record.put()

    success_output_all_parameters = """
        <p>
            <span style="font-size: larger;">
                The simulation parameters are ready to load.
            </span>
        </p>
        <p>
            To run the simulation use the following simulation code.<br>
            <b>Write it down</b> - you will need it when you report your results.
        </p>
        <p>
            <blockquote style="font-size: larger;">
                <b>%s</b>
            </blockquote>
        </p>
        """

    form_header = '<form enctype="multipart/form-data" action="/parametersform3" method="post">'

    form_ongoing_disturbance_selector= """
        <p>
            <b>Ongoing disturbance level: <b>
            <select name="disturbance_level">
                <option %s value = "0">None</option>
                <option %s value = "1">Very Low</option>
                <option %s value = "2">Low</option>
                <option %s value = "3">High</option>
                <option %s value = "4">Very High</option>
            </select>
        <p>
        """

    form_starting_matrix_map_label = """
        <b>Click on the map to select one or more cells to set the starting status:</b>
        """

    form_table_header = '<table background="/images/Terrain0_map.jpg"><tbody><td>'

    form_button = '<input type="image" name="aaa%s" src="/images/%sbutton.png" style="width: 10px; height=10px;">'

    form_table_footer = '</td></tbody></table>'

    form_cell_value_selector_header = """
        <b>Cell value:</b>
        <select name="cell_value">
            <option value = "R">Random plant type</option>
            <option value = "N">Permanent disturbance</option>
            <option value = "0">Gap (temporary)</option>
        """
    form_cell_value_selector_option = """
            <option value = "%s">%s</option>
        """

    form_cell_value_selector_footer = """
        </select>
        """

    form_assign_cells_button = """
        <input type="submit" name="submit_value" value="Apply cell value to cells">
        """

    form_assign_area_button = """
        <input type="submit" name="submit_value" value="Apply cell value to area">
        """

    form_submit_button = """
        <br><br><input type="submit" name="submit_value" value="Submit parameters">
        """

    form_active_hidden_fields = """
        <input type="hidden" name="selected" value="%s">
        <input type="hidden" name="starting_matrix" value="%s">
        """

    form_passive_hidden_fields = """
        <input type="hidden" name="water_level" value="%s">
        <input type="hidden" name="light_level" value="%s">
        <input type="hidden" name="temperature_level" value="%s">
        """

    form_plant_code_hidden_field = """
        <input type="hidden" name="plant_code_%s" value="%s">
        """

    form_footer = '</form>'

    common_names = ['Alder',
                    'Aspen',
                    'Starthistle',
                    'Juniper',
                    'Serviceberry',
                    'Sagebrush',
                    'Sumac',
                    'Wildrose',
                    'Fern',
                    'Maple',
                    'Elderberry',
                    'Pine',
                    'Cottonwood',
                    'Willow']

class RequestPlot(webapp.RequestHandler):
    """
    Accepts data for plotting and returns an interactive dygraph-based plot.
    """
    def get(self):
        #This should only ever get called with post data but this helps with testing
        self.post()

    def post(self):
        plot_type = self.request.get('plot_type')
        simulation_id = self.request.get('simulation_id')
        if (plot_type == 'counts'):
            data_string = self.request.get('data_string')
            self.request_counts_plot(simulation_id, data_string)
        elif (plot_type == 'age'):
            data_string = self.request.get('data_string')
            self.request_ages_plot(simulation_id, data_string)
        elif (plot_type == 'biomass'):
            data_string = self.request.get('data_string')
            self.request_biomass_plot(simulation_id, data_string)
        else:
            self.response.out.write("<html><body>Invalid plot type request</body></html>")

    plot_creation_code = """
        <html>
            <head>
                <title>%s Plot</title>
                <script type="text/javascript" src="static/lib/dygraph-combined.js" charset="utf-8"></script>
            </head>
            <body>
                <div>
                    <h3>Simulation ID: %s</h3>
                </div>
                <div id="graphdiv"></div>
                <script type="text/javascript">
                    g = new Dygraph(
                        document.getElementById("graphdiv"),
                        %s,
                        {
                            rollPeriod: 1,
                            showRoller: true,
                            includeZero: true,
                            title: <b>%s</b>,
                            xlabel: <b>year</b>,
                            ylabel: <b>%s</b>,
                            legend: "always",
                            labelsSeparateLines: false,
                            labelsDivWidth: 650,
                            width: 800,
                            height: 400,
                            drawXGrid: false
                        });
                </script>
            </body>
        </html>
        """

    # Debugging this can be nasty.  Keep this example of a good plot string for testing purposes.
    plot_data_string_TEST = """
        "year,Gaps,Alder,Fern,Cottonwood,Sagebrush,Pine\\n" +
        "0,135,75,10,15,45,120\\n" + "1,163,25,45,34,23,110\\n" +
        "2,174,26,67,45,65,23\\n" + "3,120,18,75,25,64,98\\n" +
        "4,58,76,100,25,48,93\\n" + "5,138,70,97,34,35,26\\n" +
        "6,154,86,25,35,45,55\\n" + "7,220,32,22,51,43,32\\n" +
        "8,167,35,43,45,54,56\\n" + "9,120,38,64,46,75,57\\n" +
        "10,118,40,73,37,84,48\\n" + "11,55,65,10,70,110,90\\n" +
        "12,180,80,34,36,38,32\\n"
        """

    def request_counts_plot(self, simulation_id, plot_data_string):
        self.response.out.write(self.plot_creation_code % (
                                'Count',
                                simulation_id,
                                plot_data_string,
                                'Counts by Species',
                                '# of individuals'))

    def request_ages_plot(self, simulation_id, plot_data_string):
        self.response.out.write(self.plot_creation_code % (
                                'Age',
                                simulation_id,
                                plot_data_string,
                                'Average Age by Species',
                                'average age'))

    def request_biomass_plot(self, simulation_id, plot_data_string):
         self.response.out.write(self.plot_creation_code % (
                                'Biomass',
                                simulation_id,
                                plot_data_string,
                                'Biomass by Species',
                                '% of total biomass'))


class ShowParametersPage(webapp.RequestHandler):
    """
    Accepts a simulation ID and returns a summary of the parameters for that ID.
    """
    def get(self):
        page = HtmlPage()
        self.response.out.write(page.header % 'Simulation parameters')
        simulation_id = self.request.get('id')
        water_level = 2
        light_level = 2
        temperature_level = 2
        disturbance_level = 0
        #This should match the default plant types in the Unity Module
        plant_types = [1, 8, 9, 11, 13]
        plant_types_count = 5
        is_valid_id = True
        if (simulation_id != 'default'):
            data = db.GqlQuery("SELECT * FROM MeadowRecordObject WHERE id=:1",
                            simulation_id)
            if (data.count() == 1):
                # The simulation ID is valid, display the parameters
                data = data[0]
                is_valid_id = True
                water_level = data.water_level
                light_level = data.light_level
                temperature_level = data.temperature_level
                plant_types = data.plant_types.split(',')
                #remove the -1's (none's) from the list of plant types
                plant_types[:] = (value for value in plant_types if value != -1)
                plant_types_count = len(plant_types)
                disturbance_level = data.disturbance_level
                temp_starting_matrix = data.starting_matrix
                upside_down_matrix = []
                for y in range(50):
                    row = ''
                    for x in range(50):
                        row += temp_starting_matrix[y * 50 + x]
                    upside_down_matrix.append(row)
                starting_matrix = ''
                for y in range(50):
                    starting_matrix += upside_down_matrix[49 - y]
            else:
                # There is no such simulation ID (or there is more than one with that ID?)
                is_valid_id = False
                self.response.out.write(self.display_error % simulation_id)
        if (is_valid_id):
            self.response.out.write(self.display_environment_parameters %
                                    (simulation_id,
                                     self.levels[water_level],
                                     self.levels[light_level],
                                     self.levels[temperature_level],
                                     self.disturbance_levels[disturbance_level]))
            self.response.out.write(self.display_species_header)

            for i in range(0, plant_types_count):
                self.response.out.write(self.display_species %
                                        (i + 1,
                                         self.plant_names[int(plant_types[i])],
                                         self.plant_names[int(plant_types[i])]))
            self.response.out.write(self.display_species_footer)
            self.response.out.write(self.form_table_header)
            for j in range(50):
                for i in range(50):
                    index = (j * 50) + i
                    image = starting_matrix[index]
                    #image = 'R'
                    self.response.out.write(self.form_button % image)
                if (j != 49):
                    self.response.out.write('<br>')
        self.response.out.write(self.form_table_footer)
        self.response.out.write(self.form_legend)
        self.response.out.write(page.footer)



    #Conversions from the stored level integer values to human readable values
    levels = ["Lowest", "Lower", "Normal", "Higher", "Highest"]
    disturbance_levels = ["None", "Very Low","Low", "High", "Very High"]
    plant_names = [ 'Alder',
                    'Aspen',
                    'Starthistle',
                    'Juniper',
                    'Serviceberry',
                    'Sagebrush',
                    'Sumac',
                    'Wildrose',
                    'Fern',
                    'Maple',
                    'Elderberry',
                    'Pine',
                    'Cottonwood',
                    'Willow']

    display_environment_parameters = """
        <h2>Simulation Parameters</h2>
        <p>
            <b>Simulation ID:</b> %s
        </p>
        <p>
            <b>Water level:</b> %s<br>
            <b>Light level:</b> %s<br>
            <b>Temperature level:</b> %s<br>
            <b>Ongoing disturbance level:</b> %s<br>
        </p>
        """

    display_species_header = """
        <p>
            <table border="0" cellspacing="5"><tbody><tr valign="top">
        """

    display_species = """
                <td>
                    <b>Species %s:</b> %s<br>
                    <img src="/images/%s.png" height="100" width="125"/><br>
                </td>
        """

    display_species_footer = """
            </tr></tbody></table>
            <a href="/plants" target="_blank">View plant details</a><br>
        </p>
        """

    display_error = """
        <p>Simulation ID %s does not exist!</p>
        """

    form_table_header = '<b>Starting Community:</b><br><table background="/images/Terrain0_map.jpg"><tbody><td>'

    form_button = '<img src="/images/%sbutton.png" style="width: 10px; height=10px;"/>'

    form_table_footer = '</td></tbody></table>'

    form_legend = """
        <img src="/images/Rbutton.png" style="width: 10px; height=10px;"/> = Random plant<br>
        <img src="/images/Nbutton.png" style="width: 10px; height=10px;"/> = Permanent disturbance<br>
        <img src="/images/0button.png" style="width: 10px; height=10px;"/> = Gap (temporary)<br>
        <img src="/images/1button.png" style="width: 10px; height=10px;"/> = Species 1<br>
        <img src="/images/2button.png" style="width: 10px; height=10px;"/> = Species 2<br>
        <img src="/images/3button.png" style="width: 10px; height=10px;"/> = Species 3<br>
        <img src="/images/4button.png" style="width: 10px; height=10px;"/> = Species 4<br>
        <img src="/images/5button.png" style="width: 10px; height=10px;"/> = Species 5<br>
        """

# url to class mapping
application = webapp.WSGIApplication([
    ('/', ParametersFormPageOne),
    ('/parametersform2', ParametersFormPageTwo),
    ('/parametersform3', ParametersFormPageThree),
    ('/data', GetParameters),
    ('/requestplot', RequestPlot),
    ('/plants', PlantPicturesPage),
    ('/show', ShowParametersPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
