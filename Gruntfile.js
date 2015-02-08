module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    // Karma unit test config
    karma: {
      unit: {
        configFile: 'test/js/karma.conf.js',
        background: true,
        singleRun: false
      },
      continuous: {
        configFile: 'test/js/karma.conf.js',
        singleRun: true
      }
    },

    // Python nose config
    nose: {
      options: {
        include: "python"
      },
      main: {},
      coverage: {
        options: {
          with_coverage: true,
          cover_html: true,
          cover_html_dir: "test/python-coverage",
          cover_erase: true,
          cover_package: "."
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-karma');
  grunt.loadNpmTasks('grunt-nose');

  grunt.registerTask('unittest', "Run unit tests", ['karma', 'nose']);
};
