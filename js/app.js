(function() {
    'use strict';

    function $(id) {
        return document.getElementById(id);
    };

    function repaintAll() {
        var data = [];
        var max = 0;
        var temp = {};
        var coordinates = app.coordinates;

        for (var key in app.data) {
            var val = app.data[key];
            if (/^[a-z]$/.test(key)) {
                key = key.toUpperCase();
            }
            var coord = coordinates[key] || false;
            if (coord) {
                for (var s = 0; s < coord.length; s += 2) {
                    var joined = coord.slice(s, s+2).join(";");
                    if (!temp[joined]) {
                        temp[joined] = 0;
                    }
                    temp[joined] += val;
                }
            }
        }
        for (var k in temp) {
            var xy = k.split(";");
            var val = temp[k]
            data.push({x: xy[0], y: xy[1], count: val});
            if (val > max) {
                max = val;
            }
        }
        app.heatmap.store.setDataSet({max: max, data: data});
    };

    app.init = function initialize() {
        var cfg = arguments[0] || {};
        app.configure(cfg);
        repaintAll();
    };

    app.configure = function configure(cfg) {
        var config = {};
        config.element = "keyboard";
        config.radius = 40;
        config.visible = true;
        config.opacity = 40;
        app.coordinates = app.LAYOUTS[cfg.layout || "QWERTY"];
        var heatmap = h337.create(config);
        app.heatmap = heatmap;
        if (cfg.layout) {
            $("keyboard").style.backgroundImage = "url("+app.config.imgdir+"/"+cfg.layout+".png)";
        }
    };

    $("layout").onchange = function(){
        var cfg = {};
        cfg.layout = $("layout").value;
        app.heatmap.cleanup();
        app.init(cfg);
        repaintAll();
    }

    app.init({layout: $("layout").value});

})();