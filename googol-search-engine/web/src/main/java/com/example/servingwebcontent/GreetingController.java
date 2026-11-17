package com.example.servingwebcontent;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.*;

import java.rmi.Naming;

import javax.annotation.Resource;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Scope;
import org.springframework.context.annotation.ScopedProxyMode;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.context.WebApplicationContext;

@Controller
public class GreetingController {



    @GetMapping("/")
    public String redirect() {
        return "redirect:/main";
    }


    @GetMapping("/search")
    public String search(Model model, @RequestParam(name = "query", required = false) String query, @RequestParam(name = "page", required = false, defaultValue = "1") int page){

        String ip = "localhost";
        try (InputStream input = new FileInputStream("Config.properites")) {
            Properties prop = new Properties();
            prop.load(input);
            ip = prop.getProperty("searchModule");
            } catch (IOException ignored){}

        SearchInterface sInter;

        try{
            if (query != null){
                model.addAttribute("query", query);
                model.addAttribute("page", page);
                sInter = (SearchInterface) Naming.lookup("rmi://" + ip + ":1098/search");
                List<Result> resultados = sInter.search(query, page);
                model.addAttribute("res",resultados);
                return "result";
            }else{
                return "result2";
            }

        } catch (Exception e) {
            model.addAttribute("error",e);
            return "error";
        }

    }
    

    @GetMapping("/indexURL")
    public String indexURL (Model model, @RequestParam(name="url", required = false) String url){
        String ip = "localhost";
        try (InputStream input = new FileInputStream("Config.properites")) {
            Properties prop = new Properties();
            prop.load(input);
            ip = prop.getProperty("searchModule");
            } catch (IOException ignored){}

            SearchInterface sInter;

        try{
            if(url != null){
                model.addAttribute("url", url);
                sInter = (SearchInterface) Naming.lookup("rmi://" + ip + ":1098/search");
                sInter.addFirstInQueue(url);
                return "indexURL";
            }else{
                return "indexURL";
            }

        } catch (Exception e) {
            model.addAttribute("error",e);
            return "error";
        }
        

    }
    
    @GetMapping("/connections")
    public String connections (Model model, @RequestParam(name="url", required = false) String url){
        String ip = "localhost";
        try (InputStream input = new FileInputStream("Config.properites")) {
            Properties prop = new Properties();
            prop.load(input);
            ip = prop.getProperty("searchModule");
            } catch (IOException ignored){}

        SearchInterface sInter;

        try{
            if(url != null){
                model.addAttribute("url", url);
                sInter = (SearchInterface) Naming.lookup("rmi://" + ip + ":1098/search");
                HashSet<String> resultados = sInter.searchConnections(url);
                model.addAttribute("res", resultados);
                return "connections";
            }else{
                return "connections2";
            }

        } catch (Exception e) {
            model.addAttribute("error",e);
            return "error";
        }
    }
    
    @GetMapping("/main")
    public String mainPage (){
        return "main";
    }

}