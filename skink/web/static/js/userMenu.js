(function(globals, $) {

    var skink = window.skink = window.skink || {};
    skink.UserMenu = function(options) {
        this.options = $.extend({}, this.defaults, options);

        this.gatherElements();
        this.bindEvents();
    };

    skink.UserMenu.prototype = {
        defaults: {
            menuButtonSelector: 'header .authenticated > a',
            floatingMenuSelector: 'header .authenticated .menu'
        },

        gatherElements: function() {
            this.elements = this.elements || {};
            this.elements.menuButton = $(this.options.menuButtonSelector);
            this.elements.floatingMenu = $(this.options.floatingMenuSelector);
        },

        bindEvents: function() {
            this.elements.menuButton.bind('mouseenter', this.mouseEnter.bind(this));
            this.elements.floatingMenu.bind('mouseenter', this.mouseEnter.bind(this));
            this.elements.menuButton.bind('mouseleave', this.mouseLeave.bind(this));
            this.elements.floatingMenu.bind('mouseleave', this.mouseLeave.bind(this));
        },

        mouseEnter: function(ev) {
            if (this.timer) {
                clearTimeout(this.timer);
            }
            if (this.visibilityTimeout) {
                clearTimeout(this.visibilityTimeout);
            }

            this.elements.floatingMenu.css('visibility', 'visible');
            this.elements.floatingMenu.addClass('visible');
        },

        mouseLeave: function(ev) {
            this.timer = setTimeout(function() {
                this.timer = null;
                this.elements.floatingMenu.removeClass('visible');
                this.visibilityTimeout = setTimeout(function() {
                    this.visibilityTimeout = null;
                    this.elements.floatingMenu.css('visibility', 'hidden');
                }.bind(this), 200);
            }.bind(this), 500);
        }

    };

}(window, jQuery));
