import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.eclipse.rdf4j.model.Resource;
import org.eclipse.rdf4j.model.impl.TreeModel;
import org.eclipse.rdf4j.model.util.Models;
import org.eclipse.rdf4j.model.vocabulary.RDF;
import org.eclipse.rdf4j.repository.Repository;
import org.eclipse.rdf4j.repository.RepositoryConnection;
import org.eclipse.rdf4j.repository.config.RepositoryConfig;
import org.eclipse.rdf4j.repository.config.RepositoryConfigSchema;
import org.eclipse.rdf4j.repository.manager.RepositoryManager;
import org.eclipse.rdf4j.repository.manager.RepositoryProvider;
import org.eclipse.rdf4j.rio.RDFFormat;
import org.eclipse.rdf4j.rio.RDFParser;
import org.eclipse.rdf4j.rio.Rio;
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
	
	private void initialize_repository_manager(String repoID) {
		try {
			this.strServerUrl = "http://localhost:7200"; 
			this.repositoryManager  = RepositoryProvider.getRepositoryManager(this.strServerUrl);
			this.repositoryManager.initialize();
			this.repositoryManager.getAllRepositories();
			this.repository = repositoryManager.getRepository(repoID);
			System.out.println("We have successfully connected to the repository.");
			return;
		}
		catch(Throwable t){
			logger.error(WTF_MARKER, t.getMessage(), t);
		}
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
	
	
	public GraphDBserverManager() {
		this.createGraphDBRepo();
  
	}
	
	public GraphDBserverManager(String repoID) {
		this.initialize_repository_manager(repoID);
	}
	
	
	public void createGraphDBRepo() {
		try {		
			Path path = Paths.get(".").toAbsolutePath().normalize();
			String strRepositoryConfig = path.toFile().getAbsolutePath() + "/src/main/resources/graphDB.ttl";
//			String strRepositoryConfig = "/graphDB.ttl"; 
//			String strServerUrl = 
			String repoID = "graphdb-repo";
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
			this.repository = repositoryManager.getRepository("graphdb-repo");

			// Open a connection to this repository
			this.repositoryConnection = repository.getConnection();
			return;
			
			} catch (Throwable t) {
				logger.error(WTF_MARKER, t.getMessage(), t);
			}		
	}
	
	public static void main(String[] args) {
		GraphDBserverManager pcatrdf = new GraphDBserverManager("graphdb-repo");
		pcatrdf.turnoff();
		return;
	}
}