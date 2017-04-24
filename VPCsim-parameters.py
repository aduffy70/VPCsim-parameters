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

import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import time


class HtmlPage():
    """
    Class containing basic html page layout.
    """
    header = '<html><head><title>%s v2</title></head><body>'

    footer = '</body></html>'

class SpeciesInfo():
    """
    Class containing species info lookup tables.
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

    #These levels all need to correspond to the values used in the Unity module.
    #The values shown here are only used for display purposes.
    water_levels = ['High',
                    'Normal',
                    'Normal',
                    'Low',
                    'Normal',
                    'Low',
                    'Normal',
                    'Normal',
                    'High',
                    'Normal',
                    'Normal',
                    'Low',
                    'Normal',
                    'High']

    light_levels = ['Normal',
                    'Normal',
                    'Normal',
                    'Normal',
                    'Low',
                    'High',
                    'High',
                    'Low',
                    'Normal',
                    'Normal',
                    'Normal',
                    'Normal',
                    'Normal',
                    'Normal']

    temperature_levels = ['Low',
                          'Normal',
                          'Normal',
                          'Normal',
                          'Normal',
                          'Normal',
                          'Low',
                          'Normal',
                          'Normal',
                          'Normal',
                          'Normal',
                          'Normal',
                          'Normal',
                          'Normal']

    elevations = [   'Low',
                    'Mid',
                    'Mid',
                    'Mid',
                    'High',
                    'Mid',
                    'Mid',
                    'Mid',
                    'Mid',
                    'Mid',
                    'High',
                    'Mid',
                    'Low',
                    'Mid']

    lifespans = [   'Long (25 years)',
                    'Long (25 years)',
                    'Very Short (3 years)',
                    'Very Long (100 years)',
                    'Short (10 years)',
                    'Very Long (100 years)',
                    'Short (10 years)',
                    'Very Short (3 years)',
                    'Very Short (3 years)',
                    'Long (25 years)',
                    'Short (10 years)',
                    'Very Long (100 years)',
                    'Long (25 years)',
                    'Short (10 years)']

    colonizing_levels = [   'Medium',
                            'Medium',
                            'High',
                            'Low',
                            'Medium',
                            'Low',
                            'Medium',
                            'High',
                            'High',
                            'Medium',
                            'Medium',
                            'Low',
                            'Medium',
                            'Medium']

    replaces_lists = [  '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '']

    replaced_by_lists = ['',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '',
                         '']

    other_notes = [ '',
                    '',
                    'Invasive species',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '']

class MeadowRecordObject(db.Model):
    """
    Record class representing all the parameters to run a community simulation.
    """
    # Timestamp id for this record
    id = db.StringProperty()

    # CSV integers represeting the Unity3D Tree types for each of the (up to) 5 species in the community
    plant_types = db.StringProperty()

    #Water, light, temperature, and disturbance levels
    water_level = db.IntegerProperty()
    light_level = db.IntegerProperty()
    temperature_level = db.IntegerProperty()
    disturbance_level = db.IntegerProperty()

    #50x50 matrix representing the starting values for each position in the matrix
    #(R=random, N=permanent disturbance, 0=gap, 1-5=plant types)
    starting_matrix = db.TextProperty()


class ParametersFormPageOne(webapp2.RequestHandler):
    """
    First page of the two page community parameters form.
    Accessed by the user by url or hyperlink. Controls environment
    parameters, disturbance level, and species choices.
    """
    def get(self):
        page = HtmlPage()
        info = SpeciesInfo()
        self.response.out.write(page.header % 'Simulation parameters form')
        self.response.out.write(self.form_environment_settings)
        self.response.out.write(self.form_plant_choices_header)
        for i in range(1,6):
            default_selection = ['', '', '', '', '']
            default_selection[i - 1] = 'selected="selected"'
            link_option = ''
            none_option = self.form_none_option
            if (i == 1):
                link_option = self.form_plant_examples_link
                none_option = ''
            self.response.out.write(self.form_plant_choices %
                                    (i, i, none_option, info.common_names[0], default_selection[0],
                                     info.common_names[1], info.common_names[2], info.common_names[3],
                                     info.common_names[4], info.common_names[5], info.common_names[6],
                                     info.common_names[7], default_selection[1], info.common_names[8],
                                     default_selection[2], info.common_names[9], info.common_names[10],
                                     default_selection[3], info.common_names[11], info.common_names[12],
                                     default_selection[4], info.common_names[13], link_option))
        self.response.out.write(self.form_starting_distribution)
        self.response.out.write(self.form_submit_button)
        self.response.out.write(page.footer)

    form_environment_settings = """
        <form enctype="multipart/form-data" action="/parametersform2" method="post">
            <h3> Environment Settings:</h3>
            <p>&nbsp;&nbsp;&nbsp;&nbsp;
                <b>Water/moisture/precipitation level: </b>
                <select name="water_level">
                    <option value="4">Highest</option>
                    <option value="3">Higher</option>
                    <option value="2" selected="selected">Normal</option>
                    <option value="1">Lower</option>
                    <option value="0">Lowest</option>
                </select>
            </p>
            <p>&nbsp;&nbsp;&nbsp;&nbsp;
                <b>Light level: </b>
                <select name="light_level">
                    <option value="4">Highest</option>
                    <option value="3">Higher</option>
                    <option value="2" selected="selected">Normal</option>
                    <option value="1">Lower</option>
                    <option value="0">Lowest</option>
                </select>
            </p>
            <p>&nbsp;&nbsp;&nbsp;&nbsp;
                <b>Temperature level: </b>
                <select name="temperature_level">
                    <option value="4">Highest</option>
                    <option value="3">Higher</option>
                    <option value="2" selected="selected">Normal</option>
                    <option value="1">Lower</option>
                    <option value="0">Lowest</option>
                </select>
            </p>
            <p>&nbsp;&nbsp;&nbsp;&nbsp;
                <b>Ongoing disturbance level: <b>
                <select name="disturbance_level">
                    <option value= "0">None</option>
                    <option value= "1">Very Low</option>
                    <option value= "2">Low</option>
                    <option value= "3">High</option>
                    <option value= "4">Very High</option>
                </select>
            <p><br>
    """

    form_plant_choices_header = """
        <h3>Species Settings:</h3>
        <p>
            <b>Select plant species to include in the community.</b>
        </p>
        """

    form_plant_choices = """
        <p>&nbsp;&nbsp;&nbsp;&nbsp;
            Species %s
            <select name="plant_code_%s">
                %s
                <option value = "0">%s</option>
                <option value = "1" %s>%s</option>
                <option value = "2">%s</option>
                <option value = "3">%s</option>
                <option value = "4">%s</option>
                <option value = "5">%s</option>
                <option value = "6">%s</option>
                <option value = "7">%s</option>
                <option value = "8" %s>%s</option>
                <option value = "9" %s>%s</option>
                <option value = "10">%s</option>
                <option value = "11" %s>%s</option>
                <option value = "12">%s</option>
                <option value = "13" %s>%s</option>
            </select>
            %s
        """

    form_none_option = '<option value = "-1">**None**</option>'

    form_plant_examples_link = '<a href="/plants" target="_blank">View examples</a>'


    form_starting_distribution = """
        </p>
        <p>
            <b>Select how the plants should be distributed in Year 0.</b>
        <p>
        <p>&nbsp;&nbsp;&nbsp;&nbsp;
            <select name="starting_distribution">
                <option value = "0">Place plants randomly</option>
                <option value = "1">Let me choose</option>
            </select>
        </p><br>
        """

    form_submit_button = '<input type="submit" name="next" value="Continue..."></form>'


class ParametersFormPageTwo(webapp2.RequestHandler):
    """
    Second page of the two page community parameters form.
    Controls the starting community.
    """
    def post(self):
        is_nonrandom_distribution = self.request.get('starting_distribution')
        if (is_nonrandom_distribution == '1'):
            #They want to choose the starting plant distribution
            self.response.out.write(self.header % ('Simulation parameters form', self.javascript))
            self.draw_form()
            self.response.out.write(self.footer)
        else:
            #They want a random distribution
            #This is poorly coded.  I'm just duplicating most of the StoreNewParametersClass!
            page = HtmlPage()
            self.response.out.write(page.header % 'Simulation parameters form')
            self.id = str(int(time.time() * 1000.0))
            self.store_record()
            self.response.out.write(self.success_output_all_parameters % self.id)
            self.response.out.write(page.footer)


    def draw_form(self):
        #Set up the default starting matrix with all Rs
        info = SpeciesInfo()
        self.response.out.write(self.form_instructions)
        self.response.out.write(self.form_header)
        self.response.out.write(self.form_table_header)
        for j in range(50):
            for i in range(50):
                index = (j * 50) + i
                self.response.out.write(self.form_button % index)
            if (j != 49):
                self.response.out.write('<br>')
        self.response.out.write(self.form_table_footer)
        plant_codes_list = []
        for i in range(1,6):
            plant_code = self.request.get('plant_code_%s' % i)
            if (plant_code != '-1'):
                plant_codes_list.append(plant_code)
        plant_codes_count = len(plant_codes_list)
        self.response.out.write(self.form_cell_value_selector_header)
        for i in range(0,plant_codes_count):
            self.response.out.write(self.form_cell_value_selector_option %
                                    (i+1, info.common_names[int(plant_codes_list[i])]))
        self.response.out.write(self.form_cell_value_selector_footer)
        self.response.out.write(self.form_assign_cells_button)
        self.response.out.write(self.form_assign_area_button)
        self.response.out.write(self.form_submit_button)
        self.response.out.write(self.form_passive_hidden_fields %
                                (self.request.get('water_level'),
                                 self.request.get('light_level'),
                                 self.request.get('temperature_level'),
                                 self.request.get('disturbance_level')))
        self.response.out.write(self.form_active_hidden_fields)
        for x in range(1, 6):
            self.response.out.write(self.form_plant_code_hidden_field %
                                    (x, self.request.get('plant_code_%s' % x)))
        self.response.out.write(self.form_footer)
        self.response.out.write(self.footer)

    def store_record(self):
        # Get a db record instance to hold the form data
        record = MeadowRecordObject()
        # Store a timestamp as the record id
        record.id = self.id
        # Store the water_level, light_level, and temperature_level,
        # disturbance_level and list of plant_species.
        record.water_level = int(self.request.get('water_level'))
        record.light_level = int(self.request.get('light_level'))
        record.temperature_level = int(self.request.get('temperature_level'))
        record.disturbance_level = int(self.request.get('disturbance_level'))
        plant_codes_list = []
        for i in range(1,6):
            plant_code = self.request.get('plant_code_%s' % i)
            if (plant_code != '-1'):
                plant_codes_list.append(plant_code)
        record.plant_types = ''
        if (len(plant_codes_list) != 0):
            record.plant_types = ','.join(plant_codes_list)
        # Store a community matrix of all 'R's
        record.starting_matrix = ''
        for i in range(2500):
            record.starting_matrix += 'R'
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
                <h2>%s</h2>
        """


    javascript = """
        <script type="text/javascript">

        var m_matrix = [];
        for (var cell=0; cell<2500; cell++)
            m_matrix[cell] = "R";
        var m_selected = [];

        function Load()
        {
            document.getElementById("starting_matrix").value = m_matrix.join("");
        }

        function ChangeButton(button)
        {
            if (button.getAttribute("src") != "/images/selectedbutton.png")
            {
                button.src = "/images/selectedbutton.png";
                m_selected.push(button.getAttribute("id"));
            }
            else
            {
                button.src = "/images/" + m_matrix[button.getAttribute("id")] + "button.png";
                var newindex = m_selected.indexOf(button.getAttribute("id"));
                m_selected.splice(newindex, 1);
            }
            var selected_cells = m_selected.length;
            if (selected_cells > 0)
            {
                document.getElementById("assign_cells").disabled = "";
                if (selected_cells == 2)
                {
                    document.getElementById("assign_area").disabled = "";
                }
                else
                {
                    document.getElementById("assign_area").disabled = "disabled";
                }
            }
            else
            {
                document.getElementById("assign_cells").disabled = "disabled";
            }
        }

        function ApplyValueToCells()
        {
            var cell_value = document.getElementById("cell_value").value;
            for (var i=0; i<m_selected.length; i++)
            {
                m_matrix[m_selected[i]] = cell_value;
                document.getElementById(m_selected[i]).src = "/images/" + cell_value + "button.png";
            }
            m_selected = [];
            document.getElementById('starting_matrix').value = m_matrix.join("");
        }

        function ApplyValueToArea()
        {
            var cell_value = document.getElementById("cell_value").value;
            var corner1 = m_selected[0];
            var corner2 = m_selected[1];
            var y1 = Math.floor(corner1 / 50);
            var x1 = corner1 % 50;
            var y2 = Math.floor(corner2 / 50);
            var x2 = corner2 % 50;
            var lower_x = x1;
            var upper_x = x2;
            var lower_y = y1;
            var upper_y = y2;
            if (x1 >= x2)
            {
                lower_x = x2
                upper_x = x1
            }
            if (y1 >= y2)
            {
                lower_y = y2
                upper_y = y1
            }
            for (var y=lower_y; y<=upper_y; y++)
            {
                for (var x=lower_x; x<=upper_x; x++)
                {
                    var i = y * 50 + x;
                    m_matrix[i] = cell_value;
                    document.getElementById(i.toString()).src = "/images/" + cell_value + "button.png";
                }
            }
            m_selected = [];
            document.getElementById('starting_matrix').value = m_matrix.join("");
        }
        </script>
        """

    header = '<html><head><title>%s</title>%s</head><body onload="Load()">'

    form_instructions = """
        <h3>Year 0 plant distribution:</h3>
        <b><a href="/map-help" target="_blank">Need help?</a></b>
        """

    form_header = '<form enctype="multipart/form-data" action="/newparameters" method="post">'

    form_table_header = '<table background="/images/Terrain0_map.jpg"><tbody><td>'

    form_button = '<img id="%s" src="/images/Rbutton.png" onclick="ChangeButton(this); return false;" style="width: 10px; height=10px;">'

    form_table_footer = '</td></tbody></table>'

    form_cell_value_selector_header = """
        <b>Cell value:</b>
        <select id="cell_value">
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
        <input type="button" id="assign_cells" disabled="disabled" onclick="ApplyValueToCells(); return false;" value="Apply cell value to cells">
        """

    form_assign_area_button = """
        <input type="button" id="assign_area" disabled="disabled" onclick="ApplyValueToArea(); return false;" value="Apply cell value to area">
        """

    form_submit_button = """
        <br><br><input type="submit" name="submit_value" value="Continue...">
        """

    form_passive_hidden_fields = """
        <input type="hidden" name="water_level" value="%s">
        <input type="hidden" name="light_level" value="%s">
        <input type="hidden" name="temperature_level" value="%s">
        <input type="hidden" name="disturbance_level" value="%s">
        """

    form_active_hidden_fields = """
        <input type="hidden" id="starting_matrix" name="starting_matrix" value="">
        """

    form_plant_code_hidden_field = """
        <input type="hidden" name="plant_code_%s" value="%s">
        """

    form_footer = '</form>'

    footer = '</body></html>'


class StoreNewParameters(webapp2.RequestHandler):
    def post(self):
        page = HtmlPage()
        self.response.out.write(page.header % 'Simulation parameters form')
        self.id = str(int(time.time() * 1000.0))
        self.store_record()
        self.response.out.write(self.success_output_all_parameters % self.id)
        self.response.out.write(page.footer)

    def store_record(self):
        # Get a db record instance to hold the form data
        record = MeadowRecordObject()
        # Store a timestamp as the record id
        record.id = self.id
        # Store the water_level, light_level, and temperature_level,
        # disturbance_level and list of plant_species.
        record.water_level = int(self.request.get('water_level'))
        record.light_level = int(self.request.get('light_level'))
        record.temperature_level = int(self.request.get('temperature_level'))
        record.disturbance_level = int(self.request.get('disturbance_level'))
        plant_codes_list = []
        for i in range(1,6):
            plant_code = self.request.get('plant_code_%s' % i)
            if (plant_code != '-1'):
                plant_codes_list.append(plant_code)
        record.plant_types = ''
        if (len(plant_codes_list) != 0):
            record.plant_types = ','.join(plant_codes_list)
        # Store the community matrix
        # This matrix starts with 0 in the NW corner and I need 0 in the SW corner
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
                <h2>%s</h2>
        """


class PlantPicturesPage(webapp2.RequestHandler):
    """
    Displays a page with photos of the different plant types in a new browser window.
    Accessed through links on the SetupMatrix page form.
    """
    def get(self):
        page = HtmlPage()
        info = SpeciesInfo()
        self.response.out.write(page.header % 'Species info')
        for i in range(14):
            self.response.out.write(self.plant_info_display %
                                    (info.common_names[i], info.latin_binomials[i],
                                     info.common_names[i], info.lifespans[i],
                                     info.water_levels[i], info.light_levels[i],
                                     info.temperature_levels[i], info.elevations[i],
                                     info.colonizing_levels[i], info.other_notes[i]))
        self.response.out.write(page.footer)

    plant_info_display = """
        <p>
            <big><b>%s</b></big> (<i>%s</i>)
            <table border="0"><tbody><tr valign="top">
                <td>
                    <img src="/images/%s.png" height="250" width="300"/>
                </td>
                <td>
                    <b>Maximum Lifespan:</b> %s<br>
                    <b>Optimal Environment:</b><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<b>Water:</b> %s<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<b>Light:</b> %s<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<b>Temp:</b> %s<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;<b>Elevation:</b> %s<br>
                    <b>Colonizing ability:</b> %s<br>
                    <b>Other notes:</b> %s
                </td>
            </tr></tbody></table>
        </p>
        """


class ShowParametersPage(webapp2.RequestHandler):
    """
    Accepts a simulation ID and returns a summary of the parameters for that ID.
    """
    def get(self):
        page = HtmlPage()
        info = SpeciesInfo()
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
                                         info.common_names[int(plant_types[i])],
                                         info.common_names[int(plant_types[i])]))
            self.response.out.write(self.display_species_footer)
            self.response.out.write(self.form_table_header)
            for j in range(50):
                for i in range(50):
                    index = (j * 50) + i
                    if (simulation_id != 'default'):
                        image = starting_matrix[index]
                    else:
                        image = 'R'
                    self.response.out.write(self.form_button % image)
                if (j != 49):
                    self.response.out.write('<br>')
            self.response.out.write(self.form_table_footer)
            self.response.out.write(self.form_legend)
        self.response.out.write(page.footer)

    #Conversions from the stored level integer values to human readable values
    levels = ["Lowest", "Lower", "Normal", "Higher", "Highest"]
    disturbance_levels = ["None", "Very Low","Low", "High", "Very High"]

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


class GetParameters(webapp2.RequestHandler):
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


class RequestPlot(webapp2.RequestHandler):
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
                            title: "<b>%s</b>",
                            xlabel: "<b>year</b>",
                            ylabel: "<b>%s</b>",
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


class SendCrossDomain(webapp2.RequestHandler):
    """
    Responds to crossdomain permission requests.
    """

    def get(self):
        crossdomain = '<?xml version="1.0"?>'
        crossdomain += '<cross-domain-policy>'
        crossdomain += '<allow-access-from domain="*"/>'
        crossdomain += '</cross-domain-policy>'
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write(crossdomain)

class ShowMapHelpPage(webapp2.RequestHandler):
    """
    Displays instructions for setting the starting plant distribution.
    """

    def get(self):
        page = HtmlPage()
        self.response.out.write(page.header % 'Map Instructions')
        self.response.out.write(self.instructions)
        self.response.out.write(page.footer)

    instructions = """
        <h3>Using the map to set the starting plant distribution</h3>
        <b>To put a specific plant (or gap) at specific locations:</b>
        <ol>
            <li>Click on one or more locations on the map.</li>
            <li>Select the plant type (or gap) from the drop-down menu.</li>
            <li>Click the button to <i>Apply cell value to cells</i>.</li>
            <li>Repeat 1-3 to put other plant types (or gaps) in other locations.</li>
        </ol>
        <b>To put a specific plant (or gap) in a rectangular area:</b>
        <ol>
            <li>Click on exactly two locations on the map to define the corners of a rectangular area.</li>
            <li>Select the plant type (or gap) from the drop-down menu.</li>
            <li>Click the button to <i>Apply cell value to area</i>.</li>
            <li>Repeat 1-3 to put other plant types (or gaps) in other areas.</li>
        </ol>
        <b>Note:</b> By default, any locations you leave blank will be planted at random.
        """

# url to class mapping
application = webapp2.WSGIApplication([
    ('/', ParametersFormPageOne),
    ('/parametersform2', ParametersFormPageTwo),
    ('/newparameters', StoreNewParameters),
    ('/data', GetParameters),
    ('/requestplot', RequestPlot),
    ('/plants', PlantPicturesPage),
    ('/show', ShowParametersPage),
    ('/map-help', ShowMapHelpPage),
    ('/crossdomain.xml', SendCrossDomain)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
