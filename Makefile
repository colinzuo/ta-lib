.PHONY: build

build:
	python setup.py build_ext --inplace

install:
	python setup.py install

talib/_func.pxi: tools/generate_func.py
	python tools/generate_func.py > talib/_func.pxi

talib/_stream.pxi: tools/generate_stream.py
	python tools/generate_stream.py > talib/_stream.pxi

generate: talib/_func.pxi talib/_stream.pxi

generate_clean:
	rm talib/_func.pxi talib/_stream.pxi

cython:
	cython talib/_ta_lib.pyx

cython_clean:
	rm talib/_ta_lib.c

clean:
	rm -rf build dist TA_Lib.egg*  talib/_ta_lib.*so talib/*.pyc talib/__pycache__

perf:
	python tools/perf_talib.py

test: build
	LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH} nosetests

sdist:
	python setup.py sdist --formats=gztar,zip
