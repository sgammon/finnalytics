var gulp = require('gulp'),
  sass = require('gulp-sass'),
  coffee = require('gulp-coffee'),
  svgmin = require('gulp-svgmin'),
  imagemin = require('gulp-imagemin'),
  closure = require('gulp-closure-compiler'),

  ASSET_PREFIX = 'finnalytics/assets/',

  inputs, outputs, config;

// Asset input globs.
inputs = {
  img: ASSET_PREFIX + 'img/**/*.{png,jpg,gif}',
  sass: ASSET_PREFIX + 'sass/*.sass',
  coffee: ASSET_PREFIX + 'coffee/*.coffee',
  js: ASSET_PREFIX + 'js/main.js'
};

// Asset compilation target directories.
outputs = {
  img: ASSET_PREFIX + 'img',
  css: ASSET_PREFIX + 'style',
  js: ASSET_PREFIX + 'js'
};

// Build configuration.
config = {

  // Images
  imagemin: {
    optimizationLevel: 7,
    progressive: true,
    interlaced: true,
    pngquant: true
  },

  // Sass
  sass: {
    outputStyle: 'compressed',
    sourceComments: 'map',
    sourceMap: 'sass',
    errLogToConsole: true
  },

  // Coffeescript
  coffee: {
    bare: true
  },

  // Closure Compiler
  closure: {

    // Prod compile settings
    app: {
      compilerPath: 'lib/closure/build/compiler.jar',
      fileName: outputs.js + '/app.min.js',
      compilerFlags: {
        debug: 'false',
        summary_detail_level: '3',
        warning_level: 'VERBOSE',
        language_in: 'ECMASCRIPT5',
        closure_entry_point: 'app.main',
        use_types_for_optimization: 'true',
        process_closure_primitives: 'true',
        compilation_level: 'ADVANCED_OPTIMIZATIONS'
      }
    },

    // Debug compile settings
    debug: {
      compilerPath: 'lib/closure/build/compiler.jar',
      fileName: outputs.js + '/app.debug.min.js',
      compilerFlags: {
        debug: 'true',
        summary_detail_level: '3',
        warning_level: 'VERBOSE',
        language_in: 'ECMASCRIPT5',
        formatting: 'PRETTY_PRINT',
        closure_entry_point: 'app.main',
        use_types_for_optimization: 'true',
        process_closure_primitives: 'true',
        compilation_level: 'SIMPLE_OPTIMIZATIONS'
      }
    }
  },

  // SVG minification
  svgmin: {}
};

// Compile sass source to css
gulp.task('sass', function () {
  console.log('Compiling stylesheets...');
  return gulp.src(inputs.sass)
    .pipe(sass(config.sass))
    .pipe(gulp.dest(outputs.css));
});

// Compile coffeescript source to js
gulp.task('coffee', function () {
  console.log('Compiling coffeescript to %s...', outputs.js);
  return gulp.src(inputs.coffee)
    .pipe(coffee(config.coffee).on('error', console.log))
    .pipe(gulp.dest(outputs.js));
});

// Compile JS with Closure Compiler in production mode
gulp.task('closure', function () {
  console.log('Compiling js for production with closure...');
  return gulp.src(inputs.js)
    .pipe(closure(config.closure.app))
    .pipe(gulp.dest(outputs.js));
});

// Compile JS with Closure Compiler in debug mode
gulp.task('closure:debug', function () {
  console.log('Compiling debug js with closure...');
  return gulp.src(inputs.js)
    .pipe(closure(config.closure.debug))
    .pipe(gulp.dest(outputs.js));
});

// Watch assets & recompile on change
gulp.task('watch', function (cb) {
  gulp.watch(inputs.sass, ['sass']);
  gulp.watch(inputs.coffee, ['coffee', 'closure:debug']);
  cb();
});

// Default task - runs with bare 'gulp'.
gulp.task('default', [
  'sass',
  'coffee',
  // 'closure'
]);

// Develop task
gulp.task('develop', [
  'sass',
  'coffee',
  // 'closure:debug',
  'watch'
]);