package com.example.servingwebcontent;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.UnknownHostException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Properties;
import java.util.StringTokenizer;

/**
 * Esta class, dos downloaders, são as componentes que vão obter as páginas web em paralelo, sendo estas obtidas
 *  e analisadas através da biblioteca JSOUP e depois vai atualizar o HashMap de Indexes do barrels invocando-o através
 *  do RMI
 *  */
public class Downloaders {

    static ArrayList<String> barrels = new ArrayList<>();

    /** No método Main vai começar por ter um try para se conectar aos todos barrels acedendo o através do ficheiro config.properties e guarda-los numa lista
     *O segundo try pega num barrels aleatorio para ficar à espera que haja um link na queue, caso nao haja link na queue este vai esperar. No while vai enquanto for true
     *vai criar um arraylist com todas as interfaces dos barrels disponiveis, após isso vai percorrer todos os barrels adicionando em todos a mesma informação. Este ciclo vai remover o primeiro link que foi adicionado ao urls e vai *com
     * recurso ao JSoup.connect(url).get() vai pesquisar e analisar um documento HTML da internet e encontrar data com ele,
     * neste caso sendo todas as palavras e urls. Com recurso ao StringTokenizer este vai criar um token que serpara
     * todas as palavras encontradas anteriormente pelo JSoup e separá-las conforme as delimitações escolhidas.
     * Após isso irá correr outro ciclo while que irá percorrer este token enquanto este tiver palavras e vai recorrer
     * à interface do Barrels para adicionar ao index o token seguinte, nesse urls especifico.
     * Após isso vai fazer o mesmo com os links através do Elements links que vai selecionar todos as hiperligações
     * usando o doc.selec() com a cssQuery referente às hiperligações a[href]. Nisto vai percorrer todos os links no
     * links vai adicionar à ArrayList de urls o url. Realizando primeiro um link.attr que vai transformar os elementos
     * em links. Por fim vai invocar novamente o método addConnections do Barrels que vai adicionar a todos os links o url
     * primário.
     * Por fim no catch vai dar catch ao erro IOException que irá ser chamada quando há erro de inputs e outputs.
     */


    public static void main(String args[]) throws RemoteException, InterruptedException {



            try (InputStream input = new FileInputStream("src/com/example/servingwebcontent/Config.properties")) {
                Properties prop = new Properties();
                prop.load(input);
                barrels.addAll(Arrays.asList(prop.getProperty("barrels").split(";")));
            } catch (IOException e) {
                e.printStackTrace();
            }
            System.out.println("Downloaders is connected.");

            try{
                String x = randomizar("barrels");
                BarrelInterface inter = (BarrelInterface) Naming.lookup("rmi://" + x );

                while(true){
                    if (inter.QueueNumber() == 0){
                        Thread.sleep(100);
                    }else{
                        break;
                    }
                }
            }catch(NotBoundException | MalformedURLException e) {
                e.printStackTrace();
            }

            BarrelInterface inter;

            while(true){


                try {
                    ArrayList<BarrelInterface> activeBarrels = new ArrayList<>();
                    for (String singleB: barrels){
                        inter = (BarrelInterface) Naming.lookup("rmi://" + singleB);
                        activeBarrels.add(inter);
                    }
                    for(BarrelInterface interB : activeBarrels){
                        String url = interB.getUrl();                 //url = urlPage
                        Document doc = Jsoup.connect(url).get();

                        StringTokenizer tokens = new StringTokenizer(doc.text(), " ,;.:/!?");


                        while (tokens.hasMoreElements()){
                            interB.addToIndex(tokens.nextToken().toLowerCase(), url);
                        }

                        Elements links = doc.select("a[href]");
                        for (Element link : links){                      // link = urlMencioned
                            interB.addToQueue(link.attr("abs:href"));
                            interB.addConnections(url,link.attr("abs:href"));
                        }

                    }



                } catch (NotBoundException | IOException e) {
                    throw new RuntimeException(e);
                }

            }

    }



    /** O método randomizer vai permitir randomizar o ip que vai ser escolhido quer no barrels quer no search Module.
     *  Este método vai se ligar ao ficheiro config.properties e escolher a componente consoante a string x for, ou
     *  search module ou barrels. O properties vai dar load ao ficheiro e vai chamar as properties, separando cada um
     *  dos ips ";".
     * @param x String que vamos querer para saber o que randomizar (barrels ou search module)
     * @return vai dar return da lista de strings com o numero random entre 0 e o numero de ips no config.properties.
     */
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

}
