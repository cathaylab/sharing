'use strict';
var gulp= require('gulp');
var $ = require('gulp-load-plugins')();
var imageminPngquant = require('imagemin-pngquant');
var imageminMozjpeg = require('imagemin-mozjpeg');

gulp.task('libjs', function () {
	gulp.src('src/lib/*.js')
		.pipe($.changed('dist/lib'))
		.pipe(gulp.dest('dist/lib'))
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

gulp.task('default', function() {
	gulp.watch(['src/lib/**/*.js'],['libjs']);
	gulp.watch(['src/images/**/*.jpg'],['imageminJPG']);
	gulp.watch(['src/images/**/*.png'],['imageminPNG']);
});