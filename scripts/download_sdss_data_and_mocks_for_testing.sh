# Learned how to to this from here
# https://stackoverflow.com/questions/273743/using-wget-to-recursively-fetch-a-directory-with-arbitrary-files-in-it

wget -r -nH --cut-dirs=1 --no-parent --reject="index.html*"  http://www.sos.siena.edu/~mbellis/sdss_data/ 

mv sdss_data ../test_data/.
