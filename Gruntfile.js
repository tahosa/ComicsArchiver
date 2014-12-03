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

    // PHPUnit test config
    phpunit: {
      classes: {
        dir: 'test/php/'
      },
      options: {
        bin: 'node_modules/grunt-phpunit/vendor/bin/phpunit',
        colors: true
      }
    }
  });

  grunt.loadNpmTasks('grunt-karma');
  grunt.loadNpmTasks('grunt-phpunit');

  grunt.registerTask('unittest', "Run unit tests", ['karma', 'phpunit']);
};
