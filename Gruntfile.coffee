
_ = require('underscore')

module.exports = (grunt) ->

  ## ~~ load plugins ~~ ##
  grunt.loadNpmTasks 'grunt-shell'
  grunt.loadNpmTasks 'grunt-svgmin'
  grunt.loadNpmTasks 'grunt-contrib-less'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-closure-compiler'

  ## ~~ stylesheets ~~ ##
  stylemap = {
    # - top-level stylesheets - #
    "finnalytics/assets/less/main.less": "finnalytics/assets/style/main.css"
  }

  less_options =
    compress: true
    cleancss: true
    ieCompat: false
    report: 'min'
    optimization: 2
    paths: ["finnalytics/assets/less"]
    sourceMap: true
    sourceMapBasepath: ".develop/maps"
    sourceMapRootpath: "/.develop/maps/"

  ## ~~ configure stuffs ~~ ##
  grunt.initConfig

    pkg: grunt.file.readJSON('package.json')

    # - Images - #
    imagemin:
      optimizationLevel: 7
      progressive: true
      interlaced: true
      pngquant: true
      files: [
        expand: true
        src: ['**/*.{png,jpg,gif}']
        cwd: 'finnalytics/assets/img/'
        dest: 'finnalytics/assets/img/'
      ]

    # - LESS - #
    less:
      base:
        files: stylemap
        options: less_options

    # - CoffeeScript - #
    coffee:

      # `app.js`
      app:
        files:
          'finnalytics/assets/js/app.js': [
            'finnalytics/assets/coffee/main.coffee'
          ]
        options:
          bare: true
          sourceMap: true
          sourceMapDir: '.develop/maps/finnalytics/assets/coffee/'

    # - Closure Compiler - #
    'closure-compiler':

      # `app.min.js`
      app:
        closurePath: "lib/closure"
        jsOutputFile: "finnalytics/assets/js/app.min.js"
        js: "finnalytics/assets/js/app.js"
        options:
          debug: false
          summary_detail_level: 3
          use_types_for_optimization: undefined
          language_in: 'ECMASCRIPT5'
          compilation_level: 'SIMPLE_OPTIMIZATIONS'
          define: [
            '"DEBUG=false"'
          ]

      # DEBUG: `app-debug.min.js`
      app_debug:
        closurePath: "lib/closure"
        jsOutputFile: "finnalytics/assets/js/app-debug.min.js"
        js: "finnalytics/assets/js/app.js"
        options:
          debug: true
          summary_detail_level: 3
          language_in: 'ECMASCRIPT5'
          compilation_level: 'SIMPLE_OPTIMIZATIONS'
          create_source_map: ".develop/maps/finnalytics/assets/js/app-debug.min.js.map"
          define: [
            '"DEBUG=true"'
          ]

    watch:
      less:
        files: ['finnalytics/assets/less/**/*.less']
        tasks: ['less']
        options:
          spawn: false
          interrupt: true

      coffee:
        files: ['finnalytics/assets/coffee/**/*.coffee']
        tasks: ['coffee']
        options:
          spawn: false
          interrupt: true

    svgmin: {}

  ## ~~ register tasks: `default` ~~ ##
  grunt.registerTask 'default', [
    'less',
    'coffee',
    'closure-compiler:app',
    'closure-compiler:app_debug'
  ]

  ## ~~ register tasks: `develop` ~~ ##
  grunt.registerTask 'develop', [
    'less',
    'coffee',
    'closure-compiler:app',
    'closure-compiler:app_debug',
    'watch'
  ]
