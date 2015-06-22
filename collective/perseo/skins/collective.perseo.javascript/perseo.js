$(document).ready(function(){
   var BASE = 'sitemap.xml.gz';
   var span = $('fieldset#fieldset-sitemapform div#formfield-form-widgets-not_included_types span.formHelp');
   var text =  span.text();
   var new_text = text.replace(BASE, '');
   span.text(new_text);
   var tag = $('<a href="' + location.href.replace('/@@perseo-settings', '/' + BASE)  + '">' + BASE + '</a>');
   span.append(tag);
});
