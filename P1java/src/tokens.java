//import things

public class tokens {
	
    // The stopword list hardcoded for you
    static String allStopWords[] = { "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
				     "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to",
				     "was", "were", "with" };


    // Helper functions start here


    public static void main(String[] args) {
	// Read arguments from command line; or use sane defaults for IDE.
	String inputZipFile = args.length >= 1 ? args[0] : "P1-train.gz";
	String outPrefix = args.length >= 2 ? args[1] : "outPrefix";
	String tokenize_type = args.length >= 3 ? args[2] : "spaces";
	String stoplist_type = args.length >= 4 ? args[3] : "yesStop";
	String stemming_type = args.length >= 5 ? args[4] : "porterStem";

	// Either put code here or call a function such as the following to do all the work
	// tokenizeFile( inputZipFile, outPrefix, tokenize_type, stoplist_type, stemming_type )
	
