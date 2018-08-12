import org.eclipse.rdf4j.model.Statement;
import org.eclipse.rdf4j.model.URI;
import org.eclipse.rdf4j.model.ValueFactory;
import org.eclipse.rdf4j.repository.RepositoryConnection;
import org.eclipse.rdf4j.repository.RepositoryException;
import org.eclipse.rdf4j.repository.util.RDFInserter;
import org.eclipse.rdf4j.rio.RDFHandler;
import org.eclipse.rdf4j.rio.RDFHandlerException;

public class ChunkCommitter implements RDFHandler {

    private final long chunkSize;
    private final RDFInserter inserter;
    private final RepositoryConnection conn;
    private final URI context;
    private final ValueFactory factory;

    private long count = 0L;

    public ChunkCommitter(RepositoryConnection conn, URI context, long chunkSize) {
        this.chunkSize = chunkSize;
        this.context = context;
        this.conn = conn;
        this.factory = conn.getValueFactory();
        inserter = new RDFInserter(conn);
    }

    public long getStatementCount() {
        return count;
    }

    @Override
    public void startRDF() throws RDFHandlerException {
        inserter.startRDF();
    }

    @Override
    public void endRDF() throws RDFHandlerException {
        inserter.endRDF();
    }

    @Override
    public void handleNamespace(String prefix, String uri)
            throws RDFHandlerException {
        inserter.handleNamespace(prefix, uri);
    }

    @Override
    public void handleStatement(Statement st) throws RDFHandlerException {
        if(context !=null) {
            st = factory.createStatement(st.getSubject(), st.getPredicate(), st.getObject(), context);
        }
        inserter.handleStatement(st);
        count++;
        // do an intermittent commit whenever the number of triples
        // has reached a multiple of the chunk size
        if (count % chunkSize == 0) {
            try {
                conn.commit();
                System.out.print(".");
            } catch (RepositoryException e) {
                throw new RDFHandlerException(e);
            }
        }
    }

    @Override
    public void handleComment(String comment) throws RDFHandlerException {
        inserter.handleComment(comment);
    }
}