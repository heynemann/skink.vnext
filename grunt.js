var execSync = require('exec-sync');

var options = {
    cssFiles: [
        'skink/web/static/css/reset.css',
        'skink/web/static/css/grid.css',
        'skink/web/static/css/fonts.css',
        'skink/web/static/css/style.css',
        'skink/web/static/css/header.css',
        'skink/web/static/css/footer.css',
        'skink/web/static/css/unauthenticated.css',
        'skink/web/static/css/no-projects.css'
    ],

    cssOutputPath: 'skink/web/static/output/skink.min.css',

    jsFiles: [
        'skink/web/static/vendor/jquery-1.8.2.js',
        'skink/web/static/js/userMenu.js',

        'skink/web/static/js/inline.js' // MUST BE THE LAST ONE
    ],

    jsOutputPath: 'skink/web/static/output/skink.min.js'
};

module.exports = function(grunt) {

    grunt.loadNpmTasks('grunt-compass');
    grunt.loadNpmTasks('grunt-css');
    grunt.loadNpmTasks('grunt-clean');

    grunt.initConfig({
        meta: {
            version: execSync("python -c 'import skink.version; print skink.version.version'"),
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
                    "adjoining-classes": false,
                    "important": false,
                    "box-sizing": false,
                    "box-model": false,
                    "known-properties": true,
                    "duplicate-background-images": true,
                    "compatible-vendor-prefixes": true,
                    "display-property-grouping": false,
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
                    "qualified-headings": false,
                    "regex-selectors": true,
                    "shorthand": true,
                    "text-indent": false,
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
            files: ['skink/web/static/scss/*.scss', 'skink/web/static/js/*.js'],
            tasks: ['dev']
        }
    });


    grunt.registerTask('dev', ['compass:dev', 'concat:css', 'concat:js']);
    grunt.registerTask('compile', ['clean', 'compass-clean', 'compass:prod', 'csslint', 'cssmin', 'lint', 'min']);
};

