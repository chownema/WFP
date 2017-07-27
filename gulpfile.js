'use strict';

// Gulp objects
var gulp = require('gulp');
var bs = require('browser-sync').create(); // create a browser sync instance.
var sass = require('gulp-sass');

// Commands
/* Sass */
var sassCmd = 'sass';
var sassSyncCmd = 'sassync';
/* Browser Sync */
var browserSyncCmd = 'bs';

// Sass
var cssDir = './website/CSS';
var scssDir = './sass/**/*.scss';

gulp.task(browserSyncCmd, function() {
    bs.init({
        server: {
            baseDir: './website'
        }
    });
});
 
gulp.task(sassCmd, function () {
  return gulp.src(scssDir)
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest(cssDir));
});
 
gulp.task(sassSyncCmd, function () {
  return gulp.src(scssDir)
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(gulp.dest(cssDir));
});

gulp.task('sass:watch', function () {
  gulp.watch('./sass/**/*.scss', ['sass']);
});