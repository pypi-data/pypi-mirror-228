"""
Anatomical visualization for SckanCompare package.

License: Apache License 2.0
"""

import os
import json
import pkg_resources
import numpy as np
import plotly.graph_objects as go

from . import globals


class AntomyVis(object):
    """
    A class for creating interactive brain region visualizations using Plotly.

    Parameters
    ----------
    region_dict : dict
        Dictionary mapping region names to (x, y) coordinates.
    species : str
        The species for which the visualization is being created.

    Attributes
    ----------
    region_dict : dict
        Dictionary mapping region names to (x, y) coordinates.
    species : str
        The species for which the visualization is being created.
    SCALE : int
        Scaling factor for the visualization.
    MAX_X : int
        Maximum X coordinate.
    MAX_Y : int
        Maximum Y coordinate.
    NODE_RADIUS : float
        Radius of the node markers.
    fig : go.FigureWidget
        Plotly figure widget for visualization.

    Methods
    -------
    __init__(region_dict, species):
        Initialize the AntomyVis class.
    get_json_species_map(species=None):
        Load a JSON species mapping of region names to (x, y) coordinates for anatomical visualization.
    draw_rect(start_x, start_y, width=1, height=1, color_border="#4051BF", color_fill="#C5CAE9", tooltiptext="<set name>"):
        Draw a rectangular region on the visualization.
    draw_poly(xlist, ylist, color_border="#4051BF", color_fill="#C5CAE9", tooltiptext="<set name>"):
        Draw a polygonal region on the visualization.
    draw_background():
        Draw the anatomical background for species.
    mark_node(region, color_border="#FF0000", color_fill="#FFFF00", small=False):
        Mark a node (brain region) on the visualization.
    interpolate_coordinates(point1, point2, resolution=0.1):
        Interpolate between two cartesian coordinates using NumPy.
    plot_dataframe(df):
        Plot dataframe connectivity info.
    draw_edge_AB(region1, region2, neuron=None):
        Draw an edge (connection) between two nodes (regions) A and B.
    draw_edge_ABC(region1, region2, region3, neuron=None):
        Draw an edge (connection) between nodes (regions) A and B via C.
    show_figure():
        Display the Plotly figure widget.
    get_figure():
        Get the Plotly figure widget.
    """

    def __init__(self, species):
        """
        Initialize the AntomyVis class.

        Parameters
        ----------
        species : str
            The species for which the visualization is being created.
        """
        if not species:
            raise ValueError("species needs to be specified!")
        if species not in globals.AVAILABLE_SPECIES_MAPS.keys():
            raise ValueError("Not currently implemented for species = {}!".format(species))
        
        self.species = species
        # get the species specific visual region mapping (X,Y)
        self.region_dict = self.get_json_species_map(species)

        self.SCALE = 50
        self.MAX_X = 43
        self.MAX_Y = 18
        self.NODE_RADIUS = 0.2

        self.fig = go.FigureWidget()
        self.fig.layout.hovermode = 'closest'
        self.fig.layout.hoverdistance = -1 # ensures no "gaps" for selecting sparse data

        self.fig.update_xaxes(showgrid=False, zeroline=False, visible=False, showticklabels=False)
        self.fig.update_yaxes(showgrid=False, zeroline=False, visible=False, showticklabels=False)
        self.fig.update_layout(showlegend=False)
        self.fig.update_yaxes(range = [self.MAX_Y+3, 0])
        self.fig.update_xaxes(range = [0, self.MAX_X])
        self.fig.update_layout(height=int(500))

        # draw the anatomical background corresponding to the species
        self.draw_background(species)

    def get_json_species_map(self, species=None):
        """
        Load a JSON species mapping of region names to (x, y) coordinates for anatomical visualization.

        Parameters
        ----------
        species : str, optional
            The species for which to load the map.

        Returns
        -------
        dict
            Dict with mapping of regions to their X,Y anatomical mapping.

        Raises
        ------
        ValueError
            If an invalid species is specified.
        """
        if not species:
            raise ValueError("species needs to be specified!")
        if species not in globals.AVAILABLE_SPECIES_MAPS.keys():
            raise ValueError("{} visual map not currently available!".format(species))
        
        datapath = pkg_resources.resource_filename("sckan_compare", "data")
        filepath = os.path.join(datapath, globals.AVAILABLE_SPECIES_MAPS[species])
        with open(filepath, encoding='utf-8-sig') as json_file:
            data = json.load(json_file)

        region_dict = {}
        for item in data:
            region_dict[item["Name"]] = [int(item["X"]), int(item["Y"])]
        return region_dict

    def draw_rect(self,
                start_x,
                start_y,
                width=1,
                height=1,
                color_border="#4051BF",
                color_fill="#C5CAE9",
                tooltiptext="<set name>"):
        """
        Draw a rectangular region on the visualization.

        Parameters
        ----------
        start_x : float
            X coordinate of the starting point.
        start_y : float
            Y coordinate of the starting point.
        width : float, optional
            Width of the rectangle.
        height : float, optional
            Height of the rectangle.
        color_border : str, optional
            Border color of the rectangle.
        color_fill : str, optional
            Fill color of the rectangle.
        tooltiptext : str, optional
            Tooltip text for the rectangle.
        """
        self.fig.add_trace(go.Scatter(
            x=[start_x,start_x+width,start_x+width,start_x, start_x],
            y=[start_y,start_y,start_y+height,start_y+height, start_y],
            mode ="lines",
            fill="toself",
            line_color=color_border,
            fillcolor=color_fill,
            text=tooltiptext,
            hoveron = "fills",
            hoverinfo = "text",
            showlegend=False
        ))

    def draw_poly(self,
                xlist,
                ylist,
                color_border="#4051BF",
                color_fill="#C5CAE9",
                tooltiptext="<set name>"):
        """
        Draw a polygonal region on the visualization.

        Parameters
        ----------
        xlist : list
            List of X coordinates for polygon vertices.
        ylist : list
            List of Y coordinates for polygon vertices.
        color_border : str, optional
            Border color of the polygon.
        color_fill : str, optional
            Fill color of the polygon.
        tooltiptext : str, optional
            Tooltip text for the polygon.
        """
        self.fig.add_trace(go.Scatter(
            x=xlist,
            y=ylist,
            mode ="lines",
            fill="toself",
            line_color=color_border,
            fillcolor=color_fill,
            text=tooltiptext,
            hoveron = "fills",
            hoverinfo = "text",
            showlegend=False
        ))

    def draw_background(self, species):
        """
        Draw the anatomical background for species.
        """
        datapath = pkg_resources.resource_filename("sckan_compare", "data")
        filepath = os.path.join(datapath, globals.AVAILABLE_SPECIES_ANATOMY[species])
        with open(filepath, encoding='utf-8-sig') as json_file:
            data = json.load(json_file)

        for item in data:
            if isinstance(item[0], int):
                self.draw_rect(*item)
            else:
                self.draw_poly(*item)
        
    def mark_node(self,
                  region,
                  color_border="#FF0000",
                  color_fill="#FFFF00",
                  small=False):
        """
        Mark a node (brain region) on the visualization.

        Parameters
        ----------
        region : str
            Name of the region to mark.
        color_border : str, optional
            Border color of the marker.
        color_fill : str, optional
            Fill color of the marker.
        small : bool, optional
            Whether to use a smaller marker.
        """
        x = self.region_dict[region][0] + 0.5
        y = self.region_dict[region][1] + 0.5
        size_factor = 7 if small else 5
        self.fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode = 'markers',
            marker_symbol = 'circle',

            marker_size = int(self.SCALE/size_factor),
            marker=dict(
                color=color_fill,
                line=dict(
                    color=color_border,
                    width=2
                )
            ),
            text=region,
            hoverinfo="text",
            name=region
        ))

    def interpolate_coordinates(self, point1, point2, resolution=0.1):
        """
        Interpolate between two cartesian coordinates using NumPy.

        Parameters
        ----------
        point1 : tuple
            First cartesian coordinate (x1, y1).
        point2 : tuple
            Second cartesian coordinate (x2, y2).
        resolution : float, optional
            Interpolation resolution.

        Returns
        -------
        tuple
            Two lists of interpolated x and y coordinates.
        """
        x1, y1 = point1
        x2, y2 = point2
        
        num_steps = int(1 / resolution)
        t = np.linspace(0, 1, num_steps + 1)
        
        interpolated_x = x1 + (x2 - x1) * t
        interpolated_y = y1 + (y2 - y1) * t
        
        return list(interpolated_x), list(interpolated_y)

    def plot_dataframe(self, df):
        """
        Plot dataframe connectivity info.
        
        Parameters
        ----------
        df : pd.DataFrame
            Dataframe containing the required data.
        """
        for idx in range(df.shape[0]):
            if 'Region_C' in df.columns:
                self.add_connection(region_A=df.iloc[idx,3],
                                        region_B=df.iloc[idx,5],
                                        region_C=df.iloc[idx,7],
                                        neuron=df.iloc[idx,1])
            else:
                self.add_connection(region_A=df.iloc[idx,3],
                                        region_B=df.iloc[idx,5],
                                        neuron=df.iloc[idx,1])

    def add_connection(self, region_A=None, region_B=None, region_C=None, neuron=None):
        """
        Add a connection to a visualization object.

        Parameters
        ----------
        region_A : str, optional
            The source region of the connection.
        region_B : str, optional
            The target region of the connection.
        region_C : str, optional
            An intermediate region for connections.
        neuron : str, optional
            The associated neuron.

        Raises
        ------
        ValueError
            If required parameters are missing.
        """
        if not region_A:
            raise ValueError("region_A needs to be specified!")
        if not region_B:
            raise ValueError("region_B needs to be specified!")

        if region_C:
            # A->C->B
            self.draw_edge_ABC(region_A, region_B, region_C, neuron)
        else:
            # A->B
            self.draw_edge_AB(region_A, region_B, neuron)

    def draw_edge_AB(self,
                     region1,
                     region2,
                     neuron=None):
        """
        Draw an edge (connection) between two nodes (regions) A and B.

        Parameters
        ----------
        region1 : str
            Name of the starting region (A).
        region2 : str
            Name of the ending region (B).
        neuron : str, optional
            Name of the associated neuron.
        """
        # From A to B
        default_linewidth = 2
        x1, y1 = self.region_dict[region1]
        x2, y2 = self.region_dict[region2]
        self.mark_node(region1)
        self.mark_node(region2)
        # self.fig.add_trace(go.Scatter(
        #     x=[x1+0.5, x2+0.5],
        #     y=[y1+0.5, y2+0.5],
        #     mode = 'lines',
        #     text=neuron,
        #     meta="main",
        #     hoverinfo="text",
        #     name=neuron,
        #     line_color="#FF0000",
        #     line={"width":default_linewidth}
        # ))

        # interpolate line for adding hover text on line (to display neuron name)
        p1 = (x1+0.5, y1+0.5)
        p2 = (x2+0.5, y2+0.5)
        x_new, y_new = self.interpolate_coordinates(p1, p2)
        self.fig.add_trace(go.Scatter(
            x=x_new,
            y=y_new,
            mode = 'lines',
            text=neuron,
            hoverinfo="text",
            name=neuron,
            line_color="#FF0000",
            line={"width":default_linewidth},
            showlegend=False
        ))
        # ax.plot((x1, x2), (y1, y2), linewidth=2, color='firebrick')

    def draw_edge_ABC(self,
                      region1,
                      region2,
                      region3,
                      neuron=None):
        """
        Draw an edge (connection) between nodes (regions) A and B via C.

        Parameters
        ----------
        region1 : str
            Name of the starting region (A).
        region2 : str
            Name of the ending region (B).
        region3 : str
            Name of the intermediate region (C).
        neuron : str, optional
            Name of the associated neuron.
        """
        # From A to B via C
        default_linewidth = 2
        x1, y1 = self.region_dict[region1]
        x2, y2 = self.region_dict[region2]
        x3, y3 = self.region_dict[region3]
        self.mark_node(region1)
        self.mark_node(region2)
        self.mark_node(region3, color_border="#000000", color_fill="#00FF00", small=True)
        # self.fig.add_trace(go.Scatter(
        #     x=[x1+0.5, x3+0.5, x2+0.5],
        #     y=[y1+0.5, y3+0.5, y2+0.5],
        #     mode = 'lines',
        #     text=neuron,
        #     hoverinfo="text",
        #     name=neuron,
        #     # line_shape="spline",
        #     line_color="#FF0000",
        #     line={"width":default_linewidth}
        # ))

        # interpolate line for adding hover text on line (to display neuron name)
        # first part of line: A to C
        p1 = (x1+0.5, y1+0.5)
        p2 = (x3+0.5, y3+0.5)
        x_new, y_new = self.interpolate_coordinates(p1, p2)
        self.fig.add_trace(go.Scatter(
            x=x_new,
            y=y_new,
            mode = 'lines',
            text=neuron,
            hoverinfo="text",
            name=neuron,
            # line_shape="spline",
            line_color="#FF0000",
            line={"width":default_linewidth},
            showlegend=False
        ))

        # second part of line: C to B
        p1 = (x3+0.5, y3+0.5)
        p2 = (x2+0.5, y2+0.5)
        x_new, y_new = self.interpolate_coordinates(p1, p2)
        self.fig.add_trace(go.Scatter(
            x=x_new,
            y=y_new,
            mode = 'lines',
            text=neuron,
            hoverinfo="text",
            name=neuron,
            # line_shape="spline",
            line_color="#FF0000",
            line={"width":default_linewidth},
            showlegend=False
        ))

    def show_figure(self):
        """
        Display the Plotly figure widget.
        """
        self.fig.show(config= {'displaylogo': False})

    def get_figure(self):
        """
        Get the Plotly figure widget.

        Returns
        -------
        go.FigureWidget
            The Plotly figure widget.
        """
        return self.fig
