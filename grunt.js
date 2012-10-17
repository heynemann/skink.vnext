var FFI = require("node-ffi");
var libc = new FFI.Library(null, {
  "system": ["int32", ["string"]]
});

var run = libc.system;

var options = {
    cssFiles: [
        'skink/web/static/css/reset.css'
    ],

    cssOutputPath: 'skink/web/static/css/skink.min.css',

    jsFiles: [
        'skink/web/static/vendor/jquery-1.8.2.js'
    ],

    jsOutputPath: 'skink/web/static/js/skink.min.js'
};

module.exports = function(grunt) {

    grunt.loadNpmTasks('grunt-compass');
    grunt.loadNpmTasks('grunt-css');
    grunt.loadNpmTasks('grunt-clean');

    grunt.initConfig({
        meta: {
            version: run("python -c 'import skink.version; print skink.version.version'"),
            banner: '/*! skink - v<%= meta.version %> - ' +
                    '<%= grunt.template.today("yyyy-mm-dd") %> */'
        },

        clean: {
            css: options.cssOutputPath,
            js: options.jsOutputPath
        },

        csslint: {
            all: {
                src: "skink/web/static/css/*.css",
                rules: {
                    "import": true,
                    "adjoining-classes": true,
                    "important": true,
                    "box-sizing": true,
                    "box-model": true,
                    "known-properties": true,
                    "duplicate-background-images": true,
                    "compatible-vendor-prefixes": true,
                    "display-property-grouping": true,
                    "overqualified-elements": true,
                    "fallback-colors": true,
                    "duplicate-properties": true,
                    "empty-rules": true,
                    "errors": true,
                    "rules-count": true,
                    "ids": true,
                    "font-sizes": true,
                    "font-faces": true,
                    "gradients": true,
                    "floats": true,
                    "outline-none": true,
                    "qualified-headings": true,
                    "regex-selectors": true,
                    "shorthand": true,
                    "text-indent": true,
                    "unique-headings": true,
                    "universal-selector": true,
                    "unqualified-attributes": true,
                    "vendor-prefix": true,
                    "zero-units": true
                }
            }
        },

        lint: {
            all: ['skink/web/static/js/**/*.js']
        },

        concat: {
            css: {
                src: ['<banner>'].concat(options.cssFiles),
                dest: options.cssOutputPath
            },
            js: {
                src: ['<banner>'].concat(options.jsFiles),
                dest: options.jsOutputPath
            }
        },

        cssmin: {
            all: {
                src: ['<banner>'].concat(options.cssFiles),
                dest: options.cssOutputPath
            }
        },

        min: {
            all: {
                src: ['<banner>'].concat(options.jsFiles),
                dest: options.jsOutputPath
            }
        },

        compass: {
            dev: {
                src: 'skink/web/static/scss',
                dest: 'skink/web/static/css',
                outputstyle: 'expanded',
                linecomments: true
            },
            prod: {
                src: 'skink/web/static/scss',
                dest: 'skink/web/static/css',
                outputstyle: 'compressed',
                linecomments: false,
                forcecompile: true
            }
        },

        jshint: {
            options: {
                curly: true,
                eqeqeq: true,
                immed: true,
                latedef: true,
                newcap: true,
                noarg: true,
                sub: true,
                undef: true,
                eqnull: true,
                browser: true
            },
            globals: {
                jQuery: true
            }
        },

        watch: {
            files: ['skink/web/static/**/*.scss', 'skink/web/static/**/*.js'],
            tasks: ['dev']
        }
    });


    grunt.registerTask('dev', ['clean', 'compass-clean', 'compass:dev', 'csslint', 'concat:css', 'lint', 'concat:js']);
    grunt.registerTask('compile', ['clean', 'compass-clean', 'compass:prod', 'csslint', 'cssmin', 'lint', 'min']);
};

