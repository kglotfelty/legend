"""
A simple legend


"""



from pychips.advanced import open_undo_block, close_undo_block
from pychips import *

class Legend():
    """
    Create a legend.
    
    This class will create a legend in the upper right part of the
    current plot that will have one entry for each curve currently
    plotted curve. 
    
    >>> add_curve( [1,2], [-1,-1] )
    >>> add_curve( [1,2], [0,0], "symbol.style=square" )
    >>> ll = Legend()
    
    The curves are labeled 0 to N-1 and have the same symbol and
    line properties as the data currently being plotted.
    
    The curves in the legend box are not automatically updated if
    the symbol or line properties of the original plot are changed.  To
    update them the update method must be called
    
    >>> set_curve("crv1", "line.style=dashed")
    >>> ll = Legend()
    >>> set_curve("crv1", "line.style=solid")
    >>> ll.update()
    
    The legend exists in its own ChipsFrame.  It can be repositioned
    manually if the object can be selected in the plot window.  As this can
    sometime be tricky, there is also a move() method that will 
    interactively reposition the legend.
    
    >>> ll = Legend()
    >>> ll.move()
    
    The user can then use the w,a,s,d keys to move the plot.

    The initial curve legend labels are simply the number 0 to N-1.
    These can be changed all at once using the label() method:
    
    >>> add_curve( [1,2], [-1,-1] )
    >>> add_curve( [1,2], [0,0], "symbol.style=square" )
    >>> add_curve( [1,2], [1,1], "symbol.style=circle" )
    >>> ll = Legend()    
    >>> ll.label( ["Below", "Normal", "Above"] )

    
    """
    
    def __init__(self, reverse=False):

        if len( self._get_all_object_name("Window")) != 1:
            raise NotImplementedError("Must have one and only one window")
        
        if len( self._get_all_object_name("Frame")) != 1:
            raise NotImplementedError("Must have one and only one frame")

        if len( self._get_all_object_name("Plot")) != 1:
            raise NotImplementedError("Must have one and only one plot")

        if len( self._get_all_object_name("Curve")) == 0:
            raise NotImplementedError("Must have at least one curve.")

        if len( self._get_all_object_name("Curve")) >= 7:
            print("Warning: Large number of curves found.  This routine works best when there are fewer than 7 curves")
            
            
        open_undo_block()

        self._reverse = reverse
        self._get_current_curves()
        self._make_frame()
        self._make_drawing_area()
        self._background()
        self._draw()

        set_current_window( self.orig_win)
        set_current_frame( self.orig_frm)
        set_current_plot( self.orig_plot)

        close_undo_block()
        

    def _get_current_curves(self):
        """
        Get the list of curves in the current window/frame/plot.
        
        The names (labels) are saved as are the properties (get_curve)
    
        TODO: to make this work with multiple plots/window/frames, would need
            to filter the list of Curves that are associated w/ the
            current plot/window/frame.  Doable just a PITA.
        """
        self.orig_win = self._get_current_object_name("Window")  # save, make default at end
        self.orig_frm = self._get_current_object_name("Frame")  # save, make default at end
        self.orig_plot = self._get_current_object_name("Plot")  # save, make default at end

        self.usr_crvs = self._get_all_object_name("Curve") 
        self.lgnd = [ get_curve(x) for x in  self.usr_crvs ]

    def _make_frame(self):
        """
        The legend is created in a separate frame.  This makes moving it
        and show/hiding it easier.  [Not sure about resizing it though.]
        
        This creates that frame.
        
        The frame will have a red border.  We do not set the frame
        background color here.  We want to have the transparency and
        possibly fill-style be different which are not options here.
        (Transparency is only yes|no here.)
        """
        frm = ChipsFrame()
        frm.border.visible = True
        frm.border.color = "red"
        frm.stem = "Legend"
        frm.transparency = True
        frm.scale = False
        
        # This makes room for 7 curves to fit nicely.
        # More will be plotted if present, but may get squished        
        ncrv = min(len(self.lgnd)*0.075, 0.4)  
        add_frame( 0.5, 0.9-ncrv, 0.9, 0.9, frm )
        self.frm = self._get_current_object_name("Frame")

    
    def _make_drawing_area(self):
        """
        Create a plot object to draw legend.  Add plot,
        and X and Y axes.  All hidden.
        """
        plt = ChipsPlot()
        plt.bottommargin = 0.01
        plt.topmargin = 0.01
        plt.leftmargin = 0.01
        plt.rightmargin = 0.01
        plt.style = "open"
        add_plot(plt)

        ax = ChipsAxis()
        ax.automax = False
        ax.automin = False
        ax.majortick.visible = False
        ax.minortick.visible = False
        ax.offset.parallel = 0
        ax.offset.perpendicular = 0
        ax.pad = 0

        add_axis( X_AXIS, 0, 0, 3, ax )
        hide_axis()
        add_axis( Y_AXIS, 0, -1, len(self.lgnd), ax )
        hide_axis()

    def _background( self ):
        """
        Set the background of the legend.  It is a green box
        filled solid with 50% opacity.  All these can be changed -- 
        most easily via the GUI.
        """
        bg = ChipsRegion()
        bg.edge.color = "forest"
        bg.fill.color = "forest"
        bg.fill.style = "solid"
        bg.opacity = 0.5        
        add_region( [0,3,3,0], [-1, -1, len(self.lgnd),len(self.lgnd)], bg)

    @staticmethod
    def _get_point_properties( curve_properties ):
        """
        Transfer curves symbol properties to a point
        """
        pnt = ChipsPoint()
        for prop in ["angle", "color", "fill", "size", "style"]:
            setattr( pnt, prop, getattr( curve_properties, prop ))
        return pnt
        

    def _draw(self):
        """
        Draw one curve for each item in the legend
        """

        self.lgnd_crvs = []
        self.lgnd_pnts = []
        self.lgnd_lbls = []

        for ii,ll in enumerate(self.lgnd):
            if False == self._reverse:
                yy = len(self.lgnd)-ii-1
            else:
                yy = ii
            add_curve( [0.25,1], [yy,yy], self.lgnd[ii] )
            self.lgnd_crvs.append( self._get_current_object_name("Curve") )
            set_curve("symbol.style=none")
            pnt = self._get_point_properties( self.lgnd[ii].symbol )            
            add_point( 0.625, yy, pnt )
            self.lgnd_pnts.append( self._get_current_object_name("Point") )
            add_label( 1.25, yy, str(ii), "valign=0.5" )
            self.lgnd_lbls.append( self._get_current_object_name("Label") )


    def label(self, label_vals):
        """
        Relabel the legend with new values
        
        """
        
        if len(label_vals) != len(self.lgnd_lbls):
            raise RuntimeError("Number of labels does not match the number of curves")
        
        open_undo_block()
        old_frame = self._get_current_object_name("Frame")        
        set_current_frame( self.frm )
        
        for lbid,lbl in zip( self.lgnd_lbls, label_vals ):
            set_label_text( lbid, lbl )
        
        set_current_frame( old_frame )
        close_undo_block()
        
        

    def update(self):
        """
        Update the curve properties (symbole/line properties) 
        after the legend has been created
        """
        
        open_undo_block()
        old_frame = self._get_current_object_name("Frame")
        
        for usr,lgn,lpt in zip( self.usr_crvs, self.lgnd_crvs, self.lgnd_pnts):
            set_current_window( self.orig_win)
            set_current_frame( self.orig_frm)
            set_current_plot( self.orig_plot)
            cc = get_curve( usr )
            set_current_frame( self.frm )
            set_curve( lgn, cc )
            set_curve( lgn, "symbol.style=none")
            pnt = self._get_point_properties( cc.symbol )
            set_point( lpt, pnt )
        
        set_current_frame( old_frame )

        close_undo_block()
        

    
    def move(self):
        """
        Move the frame.  Can also use the GUI, but can be hard to select
        the frame "handles" to drag it around.
        
        """

        print("Make sure plot window has focus.  Use the following keys to move the legend:")
        print("  w : Up")
        print("  s : Down")
        print("  a : Left")
        print("  d : Right")
        print("  q : Quit (return to prompt)")

        open_undo_block()
        
        old_frame = self._get_current_object_name("Frame")
        set_current_frame( self.frm )
    
        cid = ChipsId()
        cid.coord_sys = PIXEL
        
        def my_move_frame( x, y):
            """
            
            """
            try:
                cid = ChipsId()
                cid.coord_sys = PIXEL
                move_frame( cid, x, y, 1 )
            except Exception as e:
                print(e)
                pass
        
        while True:
            key = get_pick( 1, KEY_PRESS )
            keyval = key[3][0]   # Yikes!
            if keyval.lower().decode("ascii") == 'w':
                my_move_frame(  0, 5 )
            elif keyval.lower().decode("ascii") == 's':
                my_move_frame(  0, -5 )
            elif keyval.lower().decode("ascii") == 'a':
                my_move_frame(  -5, 0 )
            elif keyval.lower().decode("ascii") == 'd':
                my_move_frame(  5, 0 )
            elif keyval.lower().decode("ascii") == 'q':
                break
            else:
                pass
            continue
            

        set_current_frame( old_frame )
        close_undo_block()
        

    @staticmethod
    def _get_current_object_name( name ):
        """
        We often need the chips name/id of the current object : curve, axis, etc.
        This can only be retrieved by parsing the info_current() command.
        """
        ii = info_current()
        if None == ii:
            raise RuntimeError("No {} objects to operate on".format(name))
        ii = ii.split("\n")
        ff = [x for x in ii if x.strip().startswith(name) ]
        ff = ff[-1] # last one
        name = ff.split("[")[1]
        name = name.split("]")[0]
        return name
  
    @staticmethod
    def _get_all_object_name( name ):
        """
        Similar to above, but returns all objects of that type
        """
        ii = info()
        if None == ii:
            raise RuntimeError("No {} objects to operate on".format(name))        
        ii = ii.split("\n")
        ff = [x for x in ii if x.strip().startswith(name) ]
        names = [ f.split("[")[1].split("]")[0] for f in ff ]
        return names





