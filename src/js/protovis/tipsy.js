pv.Behavior.tipsy = function(opts) {
  var tip;
  var ajaxttip;
  var ajaxThis;
  /**
   * @private When the mouse leaves the root panel, trigger a mouseleave event
   * on the tooltip span. This is necessary for dimensionless marks (e.g.,
   * lines) when the mouse isn't actually over the span.
   */
  function trigger() {
    $(tip).tipsy("hide");
  }

  /**
   * @private When the mouse leaves the tooltip, remove the tooltip span. This
   * event handler is declared outside of the event handler such that duplicate
   * registrations are ignored.
   */
  function cleanup() {
    if (tip) {
      tip.parentNode.removeChild(tip);
      tip = null;
    }
  }

  return function(d) {
      /* Compute the transform to offset the tooltip position. */
      /* Propagate the tooltip text. */
      ajaxThis = this;
        $.get('/map',{ gkey:d.nodeName,method : 'tooltip'},function(data){
        
        var t = pv.Transform.identity, p = ajaxThis.parent;
        do {
            t = t.translate(p.left(), p.top()).times(p.transform());
        } while (p = p.parent);

      /* Create and cache the tooltip span to be used by tipsy. */
      
      if (!tip) {
        var c = ajaxThis.root.canvas();
        c.style.position = "relative";
        $(c).mouseleave(trigger);

        tip = c.appendChild(document.createElement("div"));
        tip.style.position = "absolute";
        $(tip).tipsy(opts);
      }
        
      tip.title = data;
      
      if (ajaxThis.properties.width) {
        tip.style.width = Math.ceil(ajaxThis.width() * t.k) + 1 + "px";
        tip.style.height = Math.ceil(ajaxThis.height() * t.k) + 1 + "px";
      } else if (ajaxThis.properties.radius) {
        var r = ajaxThis.radius();
        t.x -= r;
        t.y -= r;
        tip.style.height = tip.style.width = Math.ceil(2 * r * t.k) + "px";
      }
      
      tip.style.left = Math.floor(ajaxThis.left() * t.k + t.x) + "px";
      tip.style.top = Math.floor(ajaxThis.top() * t.k + t.y) + "px";

      /*
       * Cleanup the tooltip span on mouseout. Immediately trigger the tooltip;
       * this is necessary for dimensionless marks.
       */
      $(tip).mouseleave(cleanup).tipsy("show");           
           
          }); 
        
      //  tip.title = this.title() || ajaxttip;//|| this.text();

      /*
       * Compute bounding box. TODO support area, lines, wedges, stroke. Also
       * note that CSS positioning does not support subpixels, and the current
       * rounding implementation can be off by one pixel.
       */
    };
};
