venv: requirements.txt
	virtualenv $@ -p `which python2.7` --clear
	$@/bin/pip install -r $<

cloudping.zip: venv cloudping.py
	cd $</lib/python2.7/site-packages/ && zip ../../../../$@ -r *
	zip --grow $@ cloudping.py

clean:
	rm -f cloudping.zip

bundle: clean cloudping.zip

.PHONY: bundle clean
