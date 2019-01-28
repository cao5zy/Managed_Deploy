rm project1/deploy/.dev -rf
python ../banyan_app_entry.py build -p project1 -c dev --build-gate --proxy-mapping="project1:/" --noauth="project2"
