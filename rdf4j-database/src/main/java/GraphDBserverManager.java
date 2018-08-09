import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Scanner;

import org.eclipse.rdf4j.model.Resource;
import org.eclipse.rdf4j.model.Statement;
import org.eclipse.rdf4j.model.impl.TreeModel;
import org.eclipse.rdf4j.model.util.Models;
import org.eclipse.rdf4j.model.vocabulary.RDF;
import org.eclipse.rdf4j.repository.Repository;
import org.eclipse.rdf4j.repository.RepositoryConnection;
import org.eclipse.rdf4j.repository.config.RepositoryConfig;
import org.eclipse.rdf4j.repository.config.RepositoryConfigSchema;
import org.eclipse.rdf4j.repository.manager.RepositoryManager;
import org.eclipse.rdf4j.repository.manager.RepositoryProvider;
import org.eclipse.rdf4j.repository.util.RDFInserter;
import org.eclipse.rdf4j.repository.util.RDFLoader;
import org.eclipse.rdf4j.rio.DatatypeHandler;
import org.eclipse.rdf4j.rio.RDFFormat;
import org.eclipse.rdf4j.rio.RDFParser;
import org.eclipse.rdf4j.rio.Rio;
import org.eclipse.rdf4j.rio.RioSetting;
import org.eclipse.rdf4j.rio.helpers.AbstractRDFHandler;
import org.eclipse.rdf4j.rio.helpers.StatementCollector;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.Marker;
import org.slf4j.MarkerFactory;

public class GraphDBserverManager {
	
	// TO CREATE A VERBOSE:
	private static Logger logger = LoggerFactory.getLogger(GraphDBserverManager.class);
	// Why This Failure marker
	private static final Marker WTF_MARKER = MarkerFactory.getMarker("WTF");
	
	String strServerUrl;
	
	// Repository variables
	RepositoryManager repositoryManager;
	Repository repository;
	RepositoryConnection repositoryConnection;
	
	// RDF Data Handlers
	private static final RioSetting<List<DatatypeHandler>> allDatatypeHandling[] = new RioSetting<List<DatatypeHandler>> {
		BasicParser
	}
    private static final RDFParser.DatatypeHandling allDatatypeHandling[] = new RDFParser.DatatypeHandling[] {
            RDFParser.DatatypeHandling.IGNORE, RDFParser.DatatypeHandling.NORMALIZE, RDFParser.DatatypeHandling.VERIFY
    };
	
	///////////////////////////////////////////
	////   INITIALIZING THE REPOSITORY     ////
	///////////////////////////////////////////
	
	public void establish_connection() {
		try {
			this.repositoryConnection = this.repository.getConnection();
			System.out.println("We have established the repository connection");
		}
		catch (Throwable t) {
			logger.error(WTF_MARKER, t.getMessage(), t);
		}	
	}
	
	private void initialize_repository_manager(String repoID) {
		try {
			this.strServerUrl = "http://localhost:7200"; 
			this.repositoryManager  = RepositoryProvider.getRepositoryManager(this.strServerUrl);
			this.repositoryManager.initialize();
			this.repositoryManager.getAllRepositories();
			System.out.println("Repository Manager has been initialized");
		}
		catch(Throwable t){
			logger.error(WTF_MARKER, t.getMessage(), t);
		}
	}
	
	private void findRepository(String repoID) {
		try {
			this.repository = this.repositoryManager.getRepository(repoID);
			System.out.println("We have successfully found the repository.");
		}
		catch(Throwable t){
			logger.error(WTF_MARKER, t.getMessage(), t);
		}
	}
	
	//Create a New GraphDB repository
	public void createGraphDBRepo(String repoID) {
		try {
			
			Path path = Paths.get(".").toAbsolutePath().normalize();
			String strRepositoryConfig = path.toFile().getAbsolutePath() + "/src/main/resources/graphDB.ttl";
//			String strRepositoryConfig = "/graphDB.ttl"; 
//			String strServerUrl = 
//			
			this.initialize_repository_manager(repoID);
//		// Instantiate a local repository manager and initialize it
//			RepositoryManager repositoryManager  = RepositoryProvider.getRepositoryManager(this.strServerUrl);
//			repositoryManager.initialize();
//			repositoryManager.getAllRepositories();

			// Instantiate a repository graph model
			TreeModel graph = new TreeModel();

			// Read repository configuration file
			InputStream config = new FileInputStream(strRepositoryConfig);
			RDFParser rdfParser = Rio.createParser(RDFFormat.TURTLE);
			rdfParser.setRDFHandler(new StatementCollector(graph));
			rdfParser.parse(config, RepositoryConfigSchema.NAMESPACE);
			config.close();

			// Retrieve the repository node as a resource
			Resource repositoryNode =  Models.subject(graph
					.filter(null, RDF.TYPE, RepositoryConfigSchema.REPOSITORY))
					.orElseThrow(() -> new RuntimeException(
								"Oops, no <http://www.openrdf.org/config/repository#> subject found!"));

			// Create a repository configuration object and add it to the repositoryManager		
			RepositoryConfig repositoryConfig = RepositoryConfig.create(graph, repositoryNode);
			this.repositoryManager.addRepositoryConfig(repositoryConfig);

			// Get the repository from repository manager, note the repository id set in configuration .ttl file
//			this.findRepository(repoID);
			
			} 
		catch (Throwable t) {
				logger.error(WTF_MARKER, t.getMessage(), t);
			}		
	}
	
	/////////////////////////////////////////
	////////    LOAD ZIPPED FILEs    ////////
	/////////////////////////////////////////
	
	public void loadZippedFile(InputStream in, RDFFormat format) {
        try {
            MyRdfInserter inserter = new MyRdfInserter(this.repositoryConnection);
            RDFLoader loader =
                    new RDFLoader(this.repositoryConnection.getParserConfig(), this.repositoryConnection.getValueFactory());
            loader.load(in, "", format, inserter);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    class MyRdfInserter extends AbstractRDFHandler {
        RDFInserter rdfInserter;
        int count = 0;

        public MyRdfInserter(RepositoryConnection con) {
            rdfInserter = new RDFInserter(con);
        }

        @Override
        public void handleStatement(Statement st) {
            count++;
            if (count % 100000 == 0)
                System.out.println("Add statement number " + count + "\n"
                        + st.getSubject().stringValue() + " "
                        + st.getPredicate().stringValue() + " "
                        + st.getObject().stringValue());
            rdfInserter.handleStatement(st);
        }
    }
    
    /// Load Multiple files from directory
    public void loadRDFdirectory(String dir) {
    	
    }
	
	public void add_data_to_rdf_nt(String filename) {
		try {
			  // start an explicit transaction to avoid each individual statement being committed
			  this.repositoryConnection.begin();
//			  String fileName = "/path/to/example.rdf";
			  RDFParser parser = Rio.createParser(Rio.getParserFormatForFileName(filename).orElse(null));
			  // add our own custom RDFHandler to the parser. This handler takes care of adding
			  // triples to our repository and doing intermittent commits
			  parser.setRDFHandler(new ChunkCommitter(this.repositoryConnection));
			  File file = new File(filename);
			  FileInputStream is = new FileInputStream(file);
			  parser.parse(is, "file://" + file.getCanonicalPath());
			  this.repositoryConnection.commit();
			}
		catch(Throwable t) {
			logger.error(WTF_MARKER, t.getMessage(), t);
		}		
	}
	
	///////////////////////////////////////
	////  SHUTTING DOWN THE REPOSITORY  ///
	///////////////////////////////////////
	
	public void turnoff() {
		// Shutdown connection, repository and manager
		try{
			System.out.println("Turning off connection to the repository");
			this.repositoryConnection.close();
			this.repository.shutDown();
			this.repositoryManager.shutDown();
			return;
		}	
		catch (Throwable t) {
			logger.error(WTF_MARKER, t.getMessage(), t);
		}		
	}
	
	///////////////////////////////////////
	////     CONSTRUCTOR METHODS     //////
	///////////////////////////////////////
	
	public GraphDBserverManager() {
		String repoID = "graphdb-pubchem";
		this.createGraphDBRepo(repoID);
		this.findRepository(repoID);
		this.establish_connection();
	}
	
	public GraphDBserverManager(String repoID) {
		this.initialize_repository_manager(repoID);
		this.findRepository(repoID);
		this.establish_connection();
	}
	
	///////////////////////////////////////
	//////  MAIN CALLER FUNCTION    ///////
	///////////////////////////////////////
	
	public static void main(String[] args) {
		GraphDBserverManager pcatrdf = new GraphDBserverManager("graphdb-pubchem");
		Scanner reader = new Scanner(System.in);
		try {
			String filename = "/Volumes/EXTERNAL/ftp.ncbi.nlm.nih.gov/pubchem/RDF/compound/general/pc_compound_role.ttl";
			dance: while(true) {
				System.out.println("1. Add a new RDF file. (Zipped Files)\n"
								  +"2. Add a directory with RDF Files. (Zipped Files)\n"
								  +"3. Query the RDF File.\n"
								  +"4. Add data using chunker.\n"
								  +"9. Adios amigo?\n"
								  + "Enter a number: ");
				int choice = reader.nextInt();
				switch(choice) {
				case 1:
//					System.out.println("Enter the Zipped File: ");
//					String filename = reader.nextLine();
//					Path path = Paths.get(".").toAbsolutePath().normalize();
//					String filename = path.toFile().getAbsolutePath() + "/src/main/resources/graphDB.ttl";
//					String filename = 
//					String filename = "/Volumes/EXTERNAL/ftp.ncbi.nlm.nih.gov/pubchem/RDF/compound/general/pc_compound_role.ttl.gz";
//					System.out.println("Enter the Triple Format");
					pcatrdf.loadZippedFile(new FileInputStream(filename), RDFFormat.TURTLE);
					break;
				case 2:
					System.out.println("Enter the directory path: ");
					String dir = reader.nextLine();
					pcatrdf.loadRDFdirectory(dir);
					break;
				case 4:
					
					pcatrdf.add_data_to_rdf_nt(filename);
					break;
				case 9:
					System.out.println("Initiating exit now");
					break dance;
				default:
					System.out.println("Try Again!");
					break;
				}
			}
			
		} 
		catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		finally {
			pcatrdf.turnoff();
			reader.close();
		}

	}
}