/**
 * Defenition file for all vendor libraries.
 *
 * This allows us to create a single bundle that we serve to the frontend
 * which includes all of the vendor libraries, rather than having to load
 * them via <script> tags all over the place.
 *
 * This is generated via the `npm run vendor` command, the full script can be
 * seen in package.json. Using browserify and uglify, we create a minified
 * bundle in the app/static/shared/js/bundle.min.js file.
 */
