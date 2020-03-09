const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
var WebpackNotifierPlugin = require('webpack-notifier');

module.exports =  {
    mode: 'development',
    entry: {
        public: [
            './public/js/index.js',
            'babel-polyfill',
        ],
    },
    output: {
        filename: '[name]/build/[name].js',
        path: path.resolve(__dirname),
    },
    watch: true,
    plugins: [
        new MiniCssExtractPlugin({
            filename: "[name]/build/[name].css"
        }),
        new WebpackNotifierPlugin(),
    ],
    module: {
        rules: [
            {
                test: /\.(s*)css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'postcss-loader',
                    'sass-loader',
                ]
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                        limit: 50000,
                        outputPath: 'fonts/',
                    }
                },

            },
        ]
    },
};
