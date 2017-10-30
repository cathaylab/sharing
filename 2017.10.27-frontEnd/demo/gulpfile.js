'use strict';
// var config = require('./config.json');
var gulp= require('gulp');
var $ = require('gulp-load-plugins')();
var imageminPngquant = require('imagemin-pngquant');
var imageminMozjpeg = require('imagemin-mozjpeg');

//Event
gulp.task('sass', function () {
  return gulp.src('src/css/*.scss')
    .pipe($.plumber())
	.pipe($.sourcemaps.init())
	.pipe($.sass({outputStyle: 'compressed'}).on('error', $.sass.logError))
	.pipe($.autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
    }))
	.pipe($.sourcemaps.write('./'))
    .pipe(gulp.dest('dist/css'))
	.pipe($.connect.reload());
});
// gulp.task('js', function () {
// 	gulp.src('src/js/**/*.js')
// 		.pipe($.plumber())
// 		.pipe(gulp.dest('dist/js'))
// 		.pipe($.connect.reload());
// });
gulp.task('js',function(){
    return gulp.src('src/js/**/*.js')
    	.pipe($.plumber())
    	.pipe($.sourcemaps.init())
		.pipe($.babel({
			presets: ['es2015']
		}))
		.pipe($.concat("app.js"))
    	.pipe($.uglify())
	    .pipe($.sourcemaps.write())
	    .pipe(gulp.dest('dist/js'))
		.pipe($.connect.reload());
});
gulp.task('connect', function() {
  $.connect.server({
  	root: 'dist/',
  	livereload: true
  });
});
gulp.task('imageminJPG', function () {
	gulp.src('src/images/**/*.jpg')
		.pipe($.plumber())
		.pipe($.changed('dist/images'))	
		.pipe(imageminMozjpeg({quality: 90})())
		.pipe(gulp.dest('dist/images'));
});
gulp.task('imageminPNG', function () {
	gulp.src('src/images/**/*.png')
		.pipe($.plumber())
		.pipe($.changed('dist/images'))	
		.pipe(imageminPngquant({quality: '90'})())
		.pipe(gulp.dest('dist/images'));
});
gulp.task('uploadHTML', function () {
	gulp.src('src/*.html')
		.pipe($.changed('dist'))
		.pipe(gulp.dest('dist'))
		.pipe($.connect.reload());
});
gulp.task('libjs', function () {
	gulp.src('src/lib/*.js')
		.pipe($.changed('dist/lib'))
		.pipe(gulp.dest('dist/lib'))
		.pipe($.connect.reload());
});
gulp.task('uploadphp', function () {
	gulp.src('src/*.php')
		.pipe($.changed('dist'))
		.pipe(gulp.dest('dist'))
		.pipe($.connect.reload());
});
gulp.task('del',function(){
	require('del')('node_modules');
});

//AddListener
gulp.task('default',['connect'], function() {
	gulp.watch(['src/css/*.scss'],['sass']);
	gulp.watch(['src/js/**/*.js'],['js']);
	gulp.watch(['src/lib/**/*.js'],['libjs']);
	gulp.watch(['src/images/**/*.jpg'],['imageminJPG']);
	gulp.watch(['src/images/**/*.png'],['imageminPNG']);
	gulp.watch(['src/*.html'],['uploadHTML']);
	gulp.watch(['src/*.php'],['uploadphp']);
});
