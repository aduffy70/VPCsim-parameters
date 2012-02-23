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
    header = '<html><body>'

    instructions = """
        <p>
            This form generates virtual plants in a simulated plant community growing in the 3D virtual space. Changes made here will not take effect until they are enabled there.<br>
        </p>
        <hr>
        """

    footer = '</body></html>'


class LogOrParametersPage(webapp.RequestHandler):
    """
    Page to select either the parameters form or log form.
    """
    def get(self):
        page = HtmlPage()
        self.response.out.write(page.header)
        self.response.out.write(self.instructions)
        self.response.out.write(self.form)
        self.response.out.write(self.instructions_link)
        self.response.out.write(page.footer)

    instructions = """
        <p>
            <b>Welcome to the virtual plant community simulations (VPCsim) web application.</b>
        </p>
        From this page you can:
        <ul>
            <li>change the parameters controlling a virtual plant community,</li>
            <li>  </li>
        </ul>
        <hr>
        """

    form = """
        <form enctype="multipart/form-data" action="/parametersform1" method="get">
           <input type="submit" value="Change all parameters" style="width: 175px">
        </form>
        """

    instructions_link = """
        <p>
            <a href="/images/VPCsimInstructions.pdf" target="_blank">Instructions</a>
        </p>
        """

class MeadowRecordObject(db.Model):
    """
    Record class representing all the parameters to run a community simulation.
    """
    # Timestamp id for this record
    id = db.StringProperty()

    # CSV integers represeting the Unity3D Tree types for each of the 5 species in the community
    plant_types = db.StringProperty()

    #Terrain, water, light, temperature, and disturbance levels
    terrain = db.IntegerProperty()
    water_level = db.IntegerProperty()
    light_level = db.IntegerProperty()
    temperature_level = db.IntegerProperty()
    disturbance_level = db.IntegerProperty()

    #Matrix representing the starting values for each position in the matrix (R=random, N=disturbance, 0=gap, 1-5=plant types)
    starting_matrix = db.TextProperty()


class ParametersFormPageOne(webapp.RequestHandler):
    """
    First page of the three page community parameters form.  Accessed by the user by url or hyperlink. Controls terrain and environment parameters (and includes some hidden matrix parameters).
    """
    def get(self):
        page = HtmlPage()
        self.response.out.write(page.header)
        self.response.out.write(page.instructions)
        self.response.out.write(self.form)
        self.response.out.write(page.footer)

    form = """
        <form enctype="multipart/form-data" action="/parametersform2" method="post">
            <p>
                <b>Terrain map:</b> Select the terrain<br>
                <input type="radio" name="terrain" value="0" checked>
                <img src="/images/Terrain0_map.jpg" height="100" width="100" />
                &nbsp;&nbsp;
                <input type="radio" name="terrain" value="1">
                <img src="/images/Terrain1_map.jpg" height="100" width="100" />
                &nbsp;&nbsp;
                <input type="radio" name="terrain" value="2">
                <img src="/images/Terrain2_map.jpg" height="100" width="100" />
                &nbsp;&nbsp;
                <input type="radio" name="terrain" value="3">
                <img src="/images/Terrain3_map.jpg" height="100" width="100" />
                &nbsp;&nbsp;
            </p>
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
    Second page of the three page community parameters form.  Accessed by the user by submitting ParametersFormPageOne.  Controls plant settings
    """
    def post(self):
        page = HtmlPage()
        self.response.out.write(page.header)
        self.response.out.write(self.form_header)
        for i in range(1,6):
            link_option = ''
            if (i == 1):
                link_option = self.form_plant_examples_link
            self.response.out.write(self.form_plant_data % (i, i, link_option))
        self.response.out.write(self.form_hidden_fields % (self.request.get('terrain'), self.request.get('water_level'), self.request.get('light_level'), self.request.get('temperature_level')))
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
                <option value = "0">Alder</option>
                <option value = "1">Bamboo</option>
                <option value = "2">Grass</option>
                <option value = "3">Banyan</option>
                <option value = "4">Bush1</option>
                <option value = "5">Bush2</option>
                <option value = "6">Bush3</option>
                <option value = "7">Bush4</option>
                <option value = "8">Bush5</option>
                <option value = "9">Bush5a</option>
                <option value = "10">Bush6</option>
                <option value = "11">Bush6a</option>
                <option value = "12">Bush7</option>
                <option value = "13">Fern</option>
                <option value = "14">Maple</option>
                <option value = "15">Mimosa</option>
                <option value = "16">Palm</option>
                <option value = "17">Cots Pine</option>
                <option value = "18">Sycamore</option>
                <option value = "19">Willow</option>
            </select>
            %s
        """

    form_plant_examples_link = '<a href="/plants" target="_blank">View examples</a>'

    form_hidden_fields = """
        <input type="hidden" name="terrain" value="%s">
        <input type="hidden" name="water_level" value="%s">
        <input type="hidden" name="light_level" value="%s">
        <input type="hidden" name="temperature_level" value="%s">
        """

    form_submit_button = '</p><input type="submit" name="next" value="Continue..."></form>'


class GetParameters(webapp.RequestHandler):
    """
    Returns the community record with a particular timestamp as XML.  Accessed by the vMeadow opensim module.
    """
    def get(self):
        data = db.GqlQuery("SELECT * FROM MeadowRecordObject WHERE id=:1",
                            self.request.get('id'))
        self.response.out.write(data[0].to_xml())


class PlantPicturesPage(webapp.RequestHandler):
    """
    Displays a page with photos of the different plant types in a new browser window.  Accessed through links on the SetupMatrix page form.
    """
    def get(self):
        page = HtmlPage()
        self.response.out.write(page.header)
        self.response.out.write(self.picture_table)
        self.response.out.write(page.footer)

    picture_table = """
        <p>
            <b>TODO:<br>Pictures & species names are wrong.<br>This page should show a picture of each plant and provide info on lifespan, habitat/environment, and susceptibility to human disturbance.</b>
        </p>
        <table border="0">
            <tbody>
                <tr>
                    <th>Alder</th><th>Bamboo</th><th>Grass</th>
                    <th>Banyan</th><th>Bush1</th>
                </tr>
                <tr>
                    <td><img src="/images/Alder.png" height="100" width="125"/></td>
                    <td><img src="/images/Bamboo.png" height="100" width="125"/></td>
                    <td><img src="/images/Grass.png" height="100" width="125"/></td>
                    <td><img src="/images/Banyan.png" height="100" width="125"/></td>
                    <td><img src="/images/Bush1.png" height="100" width="125"/></td>
                </tr>
                <tr>
                    <td><br></td>
                </tr>
                <tr>
                    <th>Bush2</th><th>Bush3</th><th>Bush4</th>
                    <th>Bush5</th><th>Bush5a</th>
                </tr>
                <tr>
                    <td><img src="/images/Bush2.png" height="100" width="125"/></td>
                    <td><img src="/images/Bush3.png" height="100" width="125"/></td>
                    <td><img src="/images/Bush4.png" height="100" width="125"/></td>
                    <td><img src="/images/Bush5.png" height="100" width="125"/></td>
                    <td><img src="/images/Bush5a.png" height="100" width="125"/></td>
                </tr>
                <tr>
                    <td><br></td>
                </tr>
                <tr>
                    <th>Bush6</th><th>Bush6a</th><th>Bush7</th>
                    <th>Fern</th><th>Maple</th>
                </tr>
                <tr>
                    <td><img src="/images/Bush6.png" height="100" width="125"/></td>
                    <td><img src="/images/Bush6a.png" height="100" width="125"/></td>
                    <td><img src="/images/Bush7.png" height="100" width="125"/></td>
                    <td><img src="/images/Fern.png" height="100" width="125"/></td>
                    <td><img src="/images/Maple.png" height="100" width="125"/></td>
                </tr>
                <tr>
                    <td><br></td>
                </tr>
                <tr>
                    <th>Mimosa</th><th>Palm</th><th>Cots Pine</th>
                    <th>Sycamore</th><th>Willow</th>
                </tr>
                <tr>
                    <td><img src="/images/Mimosa.png" height="100" width="125"/></td>
                    <td><img src="/images/Palm.png" height="100" width="125"/></td>
                    <td><img src="/images/CotsPine.png" height="100" width="125"/></td>
                    <td><img src="/images/Sycamore.png" height="100" width="125"/></td>
                    <td><img src="/images/Willow.png" height="100" width="125"/></td>
                </tr>
            </tbody>
        </table>
        """

class ParametersFormPageThree(webapp.RequestHandler):
    """
    Page 3 of the three page parameters request form.  Accessed by submitting ParametersFormPageTwo.  Controls starting matrix and disturbance settings and stores the output from all three pages.
    """
    def post(self):
        submit_value = self.request.get('submit_value')
        if (submit_value == 'Submit parameters'):
            page = HtmlPage()
            self.response.out.write(page.header)
            self.id = str(int(time.time()))
            self.store_record()
            self.response.out.write(self.success_output_all_parameters % self.id)
            self.response.out.write(page.footer)
        else:
            self.redraw_form(submit_value)

    def redraw_form(self, submit_value):
        page = HtmlPage()
        disturbance_level = self.request.get('disturbance_level')
        terrain = self.request.get('terrain')
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
        self.response.out.write(page.header)
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
        self.response.out.write(self.form_table_header % terrain)
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
            self.response.out.write(self.form_cell_value_selector)
            self.response.out.write(self.form_assign_cells_button)
            if (len(selected) == 2):
                self.response.out.write(self.form_assign_area_button)
        else:
            self.response.out.write('<br>')
        self.response.out.write(self.form_submit_button)
        #Pass the list of selected cells, the current starting matrix, ongoing disturbance value and which terrain we are using.
        self.response.out.write(self.form_active_hidden_fields % (
            ','.join(selected),''.join(starting_matrix),terrain))
        #Pass the values from previous form pages (if we used those previous pages)
        self.response.out.write(self.form_passive_hidden_fields % (
            self.request.get('water_level'),
            self.request.get('light_level'),
            self.request.get('temperature_level')))
        for x in range(1, 6):
            self.response.out.write(self.form_plant_code_hidden_field % (x, self.request.get('plant_code_%s' % x)))
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
        # Store the terrain, water_level, light_level, and temperature_level, and list of plant_species.
        record.terrain = int(self.request.get('terrain'))
        record.water_level = int(self.request.get('water_level'))
        record.light_level = int(self.request.get('light_level'))
        record.temperature_level = int(self.request.get('temperature_level'))
        record.plant_types = ''
        for i in range(1, 6):
            comma = ','
            if (i == 5):
                comma = ''
            record.plant_types += self.request.get('plant_code_%s' % i) + comma
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
            To run the simulation use the following simulation code.<br>Write it down - you will need it when you report your results.
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

    form_table_header = '<table background="/images/Terrain%s_map.jpg"><tbody><td>'

    form_button = '<input type="image" name="aaa%s" src="/images/%sbutton.png" style="width: 10px; height=10px;">'

    form_table_footer = '</td></tbody></table>'

    form_cell_value_selector_disturbance_only = """
        <b>Cell value:</b>
        <select name="cell_value">
            <option value = "R">Not disturbed</option>
            <option value = "N">Permanent disturbance</option>
        </select>
        """

    form_cell_value_selector = """
        <b>Cell value:</b>
        <select name="cell_value">
            <option value = "R">Random plant type</option>
            <option value = "N">Permanent disturbance</option>
            <option value = "0">Gap (temporary)</option>
            <option value = "1">Plant type 1</option>
            <option value = "2">Plant type 2</option>
            <option value = "3">Plant type 3</option>
            <option value = "4">Plant type 4</option>
            <option value = "5">Plant type 5</option>
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
        <input type="hidden" name="terrain" value="%s">
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

# url to class mapping
application = webapp.WSGIApplication([
    ('/', LogOrParametersPage),
    ('/parametersform1', ParametersFormPageOne),
    ('/parametersform2', ParametersFormPageTwo),
    ('/parametersform3', ParametersFormPageThree),
    ('/data', GetParameters),
    ('/plants', PlantPicturesPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
