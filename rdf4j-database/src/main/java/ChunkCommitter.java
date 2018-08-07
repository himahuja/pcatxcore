import org.eclipse.rdf4j.model.Statement;
import org.eclipse.rdf4j.repository.RepositoryConnection;
import org.eclipse.rdf4j.repository.RepositoryException;
import org.eclipse.rdf4j.repository.util.RDFInserter;
import org.eclipse.rdf4j.rio.RDFHandler;
import org.eclipse.rdf4j.rio.RDFHandlerException;

class ChunkCommitter implements RDFHandler {
  private RDFInserter inserter;
  private RepositoryConnection conn;
  private long count = 0L;
  // do intermittent commit every 500,000 triples
  private long chunksize = 500000L;
  public ChunkCommitter(RepositoryConnection conn) {
    inserter = new RDFInserter(conn);
    this.conn = conn;
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
  public void handleNamespace(String prefix, String uri) throws RDFHandlerException {
    inserter.handleNamespace(prefix, uri);
  }
  @Override
  public void handleStatement(Statement st) throws RDFHandlerException {
    inserter.handleStatement(st);
    count++;
    // do an intermittent commit whenever the number of triples
    // has reached a multiple of the chunk size
    if (count % chunksize == 0) {
      try {
        conn.commit();
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