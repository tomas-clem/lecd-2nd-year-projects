package com.example.servingwebcontent;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.UnknownHostException;
import java.rmi.registry.LocateRegistry;
import java.rmi.server.UnicastRemoteObject;
import java.util.*;

/** O search Module é a componente visível pelo utilizador, comunicando através de RMI com os Barrels de forma a
 * satisfazer o pedido do utilizador. O SearchModule em si não vai armazenar qualquer tipo de dados pois dependende
 * dos Barrels para o fazer.
 *
 */
public class SearchModule  extends UnicastRemoteObject implements SearchInterface {

    /**O objetivo deste método é iniciar um servidor de objetos remotos Java (RMI), criando assim uma instância
     * da classe SearchModule, usando uma entrada com nome e porte que depois terá de ser inserida para ser feita uma
     * ligação.*/

    public static void main(String args[]) {
        try {
            SearchModule searchModule = new SearchModule();
            LocateRegistry.createRegistry(1098).rebind("search", searchModule);
            System.out.println("SearchModule is ready.");
        } catch (RemoteException re) {
            System.out.println("Exception in SearchModule.main: " + re);
        }

    }

    protected SearchModule() throws RemoteException {
    }

    /** O método search vai receber uma query do utilizador com termos a pesquisar e vai percorrer todos os urls e agrupa-los
     * num ArrayList caso estes tenham esse termo.
     * Primeiramente vamos estabelecer a conexão com os barrels através do Naming.lookup com os respetivos portos e nome
     * dos barrels. Após isso criamos um HashSet de Strings com recurso ao método do getURLS, criamos tambem uma arrayList
     * das pesquisas e uma lista com um Map, key-value chamado sorted elements que vai ordenar os urls com base na sua
     * relevância recorrendo ao método relevanciaURL.
     * Após isso vai percorrer todos os urls no sortedURL, dispondo-os de 10 em 10 por página. No ciclo try este vai
     * tentar conectar o jsoup utilizando a chave do url sendo o link e o .get para ter os tokens desse url.
     * Após isso vai adicionar à ArrayList da pesquisa o titulo do documento, o seu link e um pequeno paragrafo do texto
     * correspondente à primeira linha.
     * @param query os termos a pesquisar
     * @return ArrayList que vai conter todos os urls que contenham a query
     * @throws IOException
     * @throws NotBoundException
     */
    public ArrayList<Result> search(String query, int page) throws IOException, NotBoundException {

        String x = randomizar("barrels");

        BarrelInterface inter = (BarrelInterface) Naming.lookup("rmi://" + x);
        query=query.toLowerCase();
        HashSet<String> urls = getUrls(query, inter);
        ArrayList<Result> pesq = new ArrayList<Result>();


        if (urls == null){
            return new ArrayList<>();
        }


        List<Map.Entry<String,Integer>> sortedURL = relevanciaUrl(urls, inter);

        for (Map.Entry<String,Integer> url : sortedURL){
            try{
                Document doc = Jsoup.connect(url.getKey()).get();

                Element paragrafo = doc.select("p").first();

                if(paragrafo != null) {
                    Result single_pesq = new Result(doc.title(), url.getKey(), paragrafo.text());
                    pesq.add(single_pesq);
                } else{
                    Result single_pesq = new Result(doc.title(), url.getKey(), null);
                    pesq.add(single_pesq);
                }


            }catch(IOException e){
                e.printStackTrace();
            }
        }
        int start = 10*(page-1);
        int end = start+10;
        if (end > pesq.size()){
            end = pesq.size();
        }

        if (end < start){
            return new ArrayList<>();
        }

        return new ArrayList<>(pesq.subList(start, end));
    }

    /** O método get urls vai dar os urls. Este método vai receber a query e o inter e vai transformar
     * a query em stringTokenizer. Vai após isso correr um ciclo while que irá percorrer até ter percorrido todas as palavras.
     * Assim vai adicionar ao set a/as palavras e os seus respetivos links. No ciclo for este vai percorrer o numero de
     * palavras que lá estiverem e vai fazer a interseção dos links dizendo quais os links em que estão todas as palavras.
     *
     * @param query Palavras que se vão ser Stringtokenizer e se vão pesquisar os urls em que elas estão
     * @param inter A interface do Barrels que vai permitir chamar os métodos do Barrels
     * @return Lista de urls que têm as palavras escritas pelo utilizador
     * @throws RemoteException
     * @throws NotBoundException
     */
    static public HashSet<String> getUrls(String query, BarrelInterface inter) throws RemoteException {

        StringTokenizer words = new StringTokenizer(query, " ,;.:/!?");
        ArrayList<HashSet<String>> sets = new ArrayList<HashSet<String>>();

        while(words.hasMoreElements()){
            String word = words.nextToken();
            sets.add(inter.searchSingleWord(word));
        }

        for(int i = 1; sets.size()>i; i++){
            if (sets.get(i) != null)
                sets.get(0).retainAll(sets.get(i));
            else{
                sets.set(0, new HashSet<String>());
                break;
            }
        }

        return sets.get(0);
    }

    /** O método relevanciaURL vai classificar os links quanto à sua relevancia sendo mais relevante um link que está
     * mais mencionado nos outros. Este vai percorrer todos os urls duma palavra. Depois vai chamar o método .getConnections
     * dos barrels que vai dar os urls que mencionam certo url. Caso esta lista das conections tiver vazia devolve logo 0
     * e se não tiver vamos ver o size desse HashSet, que vai ser um inteiro igual ao numero de urls que lá tiverem.
     * Após isso vamos criar uma nova lista Map.Entry que vai ja ser ordenada. Para a ordenarmos vamos recorrer ao método
     * compare dentro do método relevanciaURL. Que vai simplesmente comparar o numero dos mais relevantes(os que têm mais
     * urls que os mencionam).
     *
     * @param urls lista de urls duma certa palavra
     * @param inter Interface do Barrels
     * @return Lista ordenada de urls por relevancia
     * @throws IOException
     */
    static public List<Map.Entry<String,Integer>> relevanciaUrl(HashSet<String> urls, BarrelInterface inter) throws IOException {

        HashMap<String, Integer> relevanciaUrls = new HashMap<>();

        for (String url : urls) {
            if (inter.getConnections(url) != null)
                relevanciaUrls.put(url, inter.getConnections(url).size());
            else
                relevanciaUrls.put(url, 0);

        }

        List<Map.Entry<String, Integer>> orderedList = new ArrayList<>(relevanciaUrls.entrySet());
        Collections.sort(orderedList, new Comparator<Map.Entry<String, Integer>>() {
            public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
                return o2.getValue()-o1.getValue();
            }
        });

        return orderedList;
    }

    public static String randomizar(String x){

        String[] sips = new String[0];

        try(InputStream file = new FileInputStream("src/com/example/servingwebcontent/Config.properties")){

            Properties propriedades = new Properties();
            propriedades.load(file);

            sips = propriedades.getProperty(x).split(";");



        }catch (IOException e){
            e.printStackTrace();
        }
        return sips[(int) Math.round(getRandomNumber(0,sips.length))];
    }

    /** Este método vai permitir dar um valor random entre o intervalo do valor máximo e mínimo
     * @param min Valor minimo
     * @param max Valor máximo
     * @return de um valor possível
     */
    static public int getRandomNumber(int min, int max) {
        return (int) ((Math.random() * (max - min)) + min);
    }

    /** Ao conectar ao Barrels este método permite obter o número de conexoes sem que o cliente se ligue diretamente ao
     * barrels
     *
     * @param url URL ao qual é pedido as conexões
     * @return lista de conexões associadas  ao url
     * @throws RemoteException
     */
    public HashSet<String> searchConnections(String url) throws RemoteException{
        BarrelInterface bInter;
        while(true){
            try{
                String x = randomizar("barrels");
                bInter = (BarrelInterface) Naming.lookup("rmi://" + x);
                break;
            }catch (RemoteException | NotBoundException | MalformedURLException e){
                System.out.println(e.getMessage());
            }
        }
        return bInter.getConnections(url);
    }

    /** Faz com que o cliente possa adicionar diretamente um link à queue sem se ligar diretamente com o barrels
     *
     * @param url URL a adicionar à queue
     * @throws RemoteException
     */
    public void addFirstInQueue(String url) throws RemoteException{
        BarrelInterface bInter;
        while(true){
            try{
                String x = randomizar("barrels");
                bInter = (BarrelInterface) Naming.lookup("rmi://" + x);
                break;
            }catch (RemoteException | NotBoundException | MalformedURLException e){
                System.out.println(e.getMessage());
            }
        }
        bInter.addFirstInQueue(url);
    }
}
