def main(argv):
   FILENAME = ''
   MODULE_NUMBER = ''
   COURSE_NAME = ''

   try:
      opts, args = getopt.getopt(argv,"hf:c:n:",["file=","course=","number"])
   except getopt.GetoptError:
      print sys.arv[0] +' -f <inputfile> -c "course" -n "number"'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print sys.arv[0] +' -f <inputfile> -c "course" -n "number"'
         sys.exit()
     elif opt in ("-f", "--file"):
         FILENAME = arg
     elif opt in ("-c", "--course"):
         COURSE_NAME = arg
     elif opt in ("-n", "--number"):
         MODULE_NUMBER = arg
   print 'FILENAME "', FILENAME
   print 'MODULE_NUMBER "', MODULE_NUMBER
   print 'MODULE_NUMBER "', MODULE_NUMBER


if __name__ == "__main__":
   main(sys.argv[1:])
