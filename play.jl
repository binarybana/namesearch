setup = true

if setup
    run(`unzip names.zip -d rawdata`)
end

x = csvread("rawdata/yob1880.txt")
