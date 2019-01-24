rm project1/deploy/.dev -rf
python ../banyan_app_entry.py build -p project1 -c dev --build-gate=True --proxy-mapping="project1:/"
