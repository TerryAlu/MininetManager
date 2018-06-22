echo -n > ../mount.json
mkdir -p /home/$USER/minitest/abc
echo -n '{
    "path": {
        "hh1": "/home/'$USER'/minitest/abc",
        "hh2": "/home/'$USER'/minitest"
    }
}' >> ../mount.json
sudo ../mnm --project=myproject --custom=../custom.py --topo=mytopo --mntpath=../mount.json
