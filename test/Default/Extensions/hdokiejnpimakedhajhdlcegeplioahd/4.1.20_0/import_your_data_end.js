document.title=gs("Import Your Data");document.getElementById("lp_docwrite_import_your_data1")&&set_innertext(document.getElementById("lp_docwrite_import_your_data1"),gs("Import Your Data"));document.getElementById("lp_docwrite_import_your_data2")&&set_innertext(document.getElementById("lp_docwrite_import_your_data2"),gs("Importing your data to your LastPass vault will secure it and protect you against identity theft. All imported data remains COMPLETELY confidential: the only person who can view YOUR data is YOU."));
document.getElementById("lp_docwrite_import_your_data3")&&set_innertext(document.getElementById("lp_docwrite_import_your_data3"),gs("Allow LastPass to find insecure data on your computer?"));document.getElementById("lp_docwrite_import_your_data4")&&set_innertext(document.getElementById("lp_docwrite_import_your_data4"),gs("Yes, let me choose which items I want imported into LastPass"));
document.getElementById("lp_docwrite_import_your_data5")&&set_innertext(document.getElementById("lp_docwrite_import_your_data5"),gs("No, do not import any of my insecure items"));
document.addEventListener("DOMContentLoaded",function(){window.addEventListener("unload",welcome_unload);document.getElementById("continue").addEventListener("click",function(){dounload=!1;document.getElementById("yes").checked?redirect_to_url("import.html?fromwelcome=1"):redirect_to_url("configure_formfill.html")});document.getElementById("cancel").addEventListener("click",function(){getBG().closecurrenttab("import_your_data.html")})});
