//
//import java.io.IOException;
//import java.io.InputStream;
//import java.util.Scanner;
//
//import org.eclipse.rdf4j.RDF4JException;
//import org.eclipse.rdf4j.repository.Repository;
//import org.eclipse.rdf4j.repository.RepositoryConnection;
//import org.eclipse.rdf4j.repository.RepositoryException;
//import org.eclipse.rdf4j.repository.manager.RepositoryManager;
//import org.eclipse.rdf4j.repository.manager.RepositoryProvider;
//import org.eclipse.rdf4j.rio.RDFFormat;
//import org.eclipse.rdf4j.rio.RDFParseException;
//
//public class RDF4JserverManager {
//	
//	RepositoryManager manager;
//	Repository repo;
//	RepositoryConnection conn;
//	
//	
//	
//	public RDF4JserverManager(String ID) {
////		String serverUrl = "http://128.97.46.198:8080/rdf4j-server";
//		String serverUrl = "http://localhost/rdf4j-server";
//		this.manager = RepositoryProvider.getRepositoryManager(serverUrl);
//		this.repo = manager.getRepository(ID);
//		try{
//			this.repo.initialize();
//		}
//		catch(RDF4JException e) {
//			System.out.println(e);
//			return;
//		}
//		System.out.println("The repository has been initialized.");
//	}
//
////	public RDF4JserverManager() {
////		String serverUrl = "http://128.97.46.198:8080/rdf4j-server";
////		File dataDir = new File("/path/to/datadir/");
////		Repository repo = new SailRepository(new NativeStore(dataDir));
////	}
//	public void establishConnection() {
//		Scanner reader = new Scanner(System.in);
//		try{
//			this.conn = this.repo.getConnection();
//			try {
//				while(true) {
//					System.out.println("1. Add a new RDF file.\n"
//									  +"2. Query the RDF File.\n"
//									  + "Enter a number: ");
//					int choice = reader.nextInt();
//					switch(choice) {
//					case 1:
//						this.add_new_rdf_file();
//						break;
//					case 2:
//						this.submit_query();
//						break;
//					default:
//						System.out.println("Try Again!");
//						break;
//					}
//				}
//				
//			}
////			conn.add(john, RDF.TYPE, FOAF.PERSON); // John is a person
////			conn.add(john,  RDFS.LABEL, f.createLiteral("John"));
////			RepositoryResult<Statement> statements = conn.getStatements(null, null, null);
////			// Repository result is an iteration, which allows streaming of the result in a streaming fashion
////			// can be iterated using Next() and hasNext()
////			
////			
////			Model model = QueryResults.asModel(statements);
////			
////			model.setNamespace("rdf", RDF.NAMESPACE);
////			model.setNamespace("rdfs", RDFS.NAMESPACE);
////			model.setNamespace("foaf", FOAF.NAMESPACE);
////			model.setNamespace("ex", namespace);
////			Rio.write(model, System.out, RDFFormat.TURTLE);
//			finally {
//				reader.close();
//				this.conn.close();
//			}
//		}
//		catch (RDF4JException e) {
//			System.out.println("There has been error");
//		}
//		
//	}
//	
//	private void add_new_rdf_file() {
//		System.out.println("Enter the path to the RDF file: ");
//		Scanner input = new Scanner(System.in);
//		String filename = input.nextLine();
//		try (InputStream inputstream =
//				RDF4JserverManager.class.getResourceAsStream("/" + filename)) {
//		this.conn.add(inputstream, "", RDFFormat.TURTLE);
//
//		} catch (IOException e) {
//			
//			e.printStackTrace();
//		} catch (RDFParseException e) {
//			
//			e.printStackTrace();
//		} catch (RepositoryException e) {
//			
//			e.printStackTrace();
//		}
//		
//		input.close();
//		
//	}
//	
//	private void submit_query() {
//		
//	}
//	
//	private void turnOff() {
//		this.repo.shutDown();
//	}
//
//	public static void main(String[] args) {
//		
//		String ID = "1001";
//		
//		RDF4JserverManager pcatrdf = new RDF4JserverManager(ID);
//		pcatrdf.establishConnection();
//		pcatrdf.turnOff();
//		// TODO Auto-generated method stub
////		File dataDir = new File("/media/hahuja/EXTERNAL/pcatxcoreRDF");
////		String indexes = "spoc,posc,cosp";
////		Repository rep = new SailRepository(new NativeStore(dataDir, indexes));
////		rep.initialize();
////		LocalRepositoryManager manager = new LocalRepositoryManager(dataDir);
////		manager.initialize();                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 ` /
//		
//		
////		RemoteRepositoryManager manager = new RemoteRepositoryManager(serverUrl);
////		manager.initialize()
//		
//		// This will return a remote repository manager
////				
////		Set<String> dormant = manager.getRepositoryIDs();
//		
////		Iterator<String> it2 = dormant.iterator();
////		while(it2.hasNext()) {
////			System.out.println(it2.next());
////		}
//		
//		
////		System.out.println("Hello");
//		
//		
////		rep.initialize();
//		
////		Set<String> ids = manager.getInitializedRepositoryIDs();
////		
////		Iterator<String> it = ids.iterator();
////		while(it.hasNext()) {
////			System.out.println(it.next());
////		}
////		
//		
//		
////		String namespace = "http://www.example.org/";
////		ValueFactory f = rep.getValueFactory();
//		
//		
//		//creating sample IRIs in the repository
//		
////		IRI john = f.createIRI(namespace, "john");
////		
//	
//	}
//}
//
