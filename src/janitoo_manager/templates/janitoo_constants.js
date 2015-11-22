var CAPABILITY_DESC = (function () {
    var private = {
    {% for key in capabilities %}
        '{{ capabilities[key] }}' : {{ key }},
    {% endfor %}
    };

     return {
        get: function(name) { return private[name]; }
    };
}());

var COMMAND_DESC = (function () {
    var private = {
    {% for key in commands %}
        '{{ commands[key] }}' : {{ key }},
    {% endfor %}
    };

     return {
        get: function(name) { return private[name]; }
    };
}());

var GENRE_DESC = (function () {
    var private = {
    {% for key in genres %}
        '{{ genres[key].label }}' : {{ key }},
    {% endfor %}
    };

     return {
        get: function(name) { return private[name]; }
    };
}());

var VALUE_DESC = (function () {
    var private = {
    {% for key in values %}
        '{{ values[key].label }}' : {{ key }},
    {% endfor %}
    };

     return {
        get: function(name) { return private[name]; }
    };
}());
