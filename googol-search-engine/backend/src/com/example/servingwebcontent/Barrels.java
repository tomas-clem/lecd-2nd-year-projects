package com.example.servingwebcontent;

import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;

/**
 * Esta classe serve para guardar todos os dados da aplicação recebidos pelo Java RMI (enviados pelo Downloader)
 */
public class Barrels extends UnicastRemoteObject implements BarrelInterface {

    /**
     * @param index Armazena palavras e um HashSet com os links em que essa palavra aparece
     */
    HashMap< String, HashSet<String>> index = new HashMap< String, HashSet<String>>();
    /**
     * @param connections Armazena url's e um HashSet com todos os outros url's que lhe fazem referencia
     * (url's já conhecidos)
     */
    HashMap< String, HashSet<String>> connections = new HashMap<>();

    /**
     * @param queue Armazena url's e irá funcionar como sendo a fila de espera de links para serem procurados
     */

    Deque<String> queue = new ArrayDeque<String>();


    /**
     * O objetivo deste método é iniciar um servidor de objetos remotos Java (RMI), criando assim uma instância
     * da classe Barrels, usando uma entrada com nome e porte.
     */

    public static void main(String[] args) {
        try {
            Barrels server = new Barrels();
            LocateRegistry.createRegistry(1033).rebind("servidor", server);
            System.out.println("Barrels Server is ready.");
        } catch (RemoteException re) {
            System.out.println("Exception in Barrels.main: " + re);
        }
    }

    protected Barrels() throws RemoteException {
    }

    /**
     * O método addToIndex tem como função adicionar links às palavras no HashMap index
     *
     * @param word palavra a que se quer adicionar um novo link
     * @param url link onde a palavra "word" aparece
     * @throws RemoteException
     */

    @Override
    public void addToIndex(String word, String url) throws RemoteException {
        HashSet <String> urls = index.get(word);
        if (urls == null){
            urls = new HashSet<String>();
            index.put(word,urls);
        }
        urls.add(url);
    }

    /**
     * Este método adiciona os urls da página em questão (num HashSet) aos urls que esta menciona, de modo a obter todos
     * os links em que um url é mencionado
     *
     * @param urlPage url a que estão a ser retiradas as informações (vai para os links que mencionam o outro)
     * @param urlMencioned url que é mencionado pela urlPage
     * @throws RemoteException
     */

    public void addConnections(String urlPage, String urlMencioned) throws RemoteException {
        HashSet <String> urls = connections.get(urlMencioned);
        if (urls == null){
            urls = new HashSet<String>();
            urls.add(urlPage);
            connections.put(urlMencioned,urls);
        }else
            urls.add(urlPage);
    }

    /**
     * O objetivo do método getConnections é obter todos os links que mencionam o parametro url
     *
     * @param url link ao qual se querem saber todos os outros links que o mencionam
     * @return HashSet de todos os links que mencionam o url
     * @throws RemoteException
     */

    public HashSet<String> getConnections(String url) throws RemoteException {
        return connections.get(url);
    }

    /**
     * Este método vai buscar todos os links que têm a palavra word
     *
     * @param word palavra à qual se querem encontrar todos os urls que a referem
     * @return HashSet com todos os urls que referem essa palavra
     * @throws RemoteException
     */
    @Override
    public HashSet<String> searchSingleWord(String word) throws RemoteException {
        return index.get(word);
    }

    /** Vai eliminar o primeiro da fila e depois vai return do mesmo
     * @return primeiro url da fila
     */
    public String getUrl(){
        return queue.removeFirst();
    }

    /** Vai adicionar o url à queue em ultimo
     * @param url url que vai ser adicionado
     */
    public void addToQueue(String url){
        queue.addLast(url);
    }

    /** Vai adicionar o url à queue em primeiro, ganhando assim "prioridade" aos outros
     * @param url url que vai ser adicionado
     */
    public void addFirstInQueue(String url){
        queue.addFirst(url);
    }

    /** Vai dizer o número de links que existe na queue
     */
    public  int QueueNumber(){
        return queue.size();
    }


}