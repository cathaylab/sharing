const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const autoprefixer = require('autoprefixer');

let extractStyles = new ExtractTextPlugin('css/common.css')
let extractHtml = new ExtractTextPlugin('[name].html')
let BabiliPlugin = require("babili-webpack-plugin")

let pluginsArray = [
  new webpack.LoaderOptionsPlugin({
    minimize: true,
    debug: true,
    options: {
      postcss: [
        autoprefixer({
          browsers: ['last 2 version', 'Explorer >= 10', 'Android >= 4']
        })
      ],
      sassLoader: {
        includePaths: [__dirname + '/src']
      },
      context: '/'
    }
  }),
  extractStyles,
  extractHtml,
  new webpack.HotModuleReplacementPlugin()
];

if(process.env.bulidMode === 'production') {
  pluginsArray.push(new BabiliPlugin());
}

let config = {
	context: __dirname,
	devtool: 'source-map',
	entry: {
		index: './src/js/app.js',
		// about: './src/js/about.js',
	},
	output: {
		path: __dirname + '/dist',
		// filename: 'js/[name].js'
		filename: 'js/app.js'
	},
	module: {
		rules: [
			{
				test: /\.vue$/,
				loader: 'vue-loader',
				include: __dirname + '\\src',
				options: {
					loaders: {
            scss: 'style-loader!css-loader?url=false!postcss-loader!sass-loader',
						// scss: extractStyles.extract({
            //   use: [
            //     { loader: "css-loader?sourceMap&url=false" },
            //     { loader: "postcss-loader?sourceMap" },
            //     { loader: "sass-loader?sourceMap" }
            //   ]
            // }),
          },
					postcss: [
						autoprefixer({browsers:['> 1%', 'last 2 versions', 'Firefox ESR']}),
					],
				},
			},
			{
				test: /\.pug$/,
				loader: extractHtml.extract({
					use: ['html-loader', 'pug-html-loader?pretty&exports=false']
				})
			},
			{
				test: /\.js$/,
				loader: 'babel-loader',
				include: __dirname + '\\src',
			},
			{
				test: /\.scss$/,
				loader: extractStyles.extract({
					use: [
						{ loader: "css-loader?sourceMap&url=false" },
						{ loader: "postcss-loader?sourceMap" },
						{ loader: "sass-loader?sourceMap" }
					]
				})
			},
		]
	},
	plugins: pluginsArray,
	devServer: {
		contentBase: __dirname + '/src',
		port: 9000,
		hot: true,
		inline: true,
		watchContentBase: true,
		watchOptions:{
			ignored: /images/,
		},
		proxy: {
      "/api/Event/": {
				target: "http://sonyxz1.medialand.com.tw/",
				// secure: false
				changeOrigin: true,
			}
		}
	}
};

module.exports = config;