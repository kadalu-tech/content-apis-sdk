browser:
	mkdir -p dist
	esbuild --bundle main_browser.js --outfile=./dist/kadalu-content-apis-min.js --minify

browser-no-minify:
	mkdir -p dist
	esbuild --bundle main_browser.js --outfile=./dist/kadalu-content-apis.js

node:
	esbuild main_node.js --bundle --platform=node --outfile=output_node.js
