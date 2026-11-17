package com.example.servingwebcontent;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class ServingWebContentApplication {

    @Bean
	public ServletRegistrationBean<ThymeleafServlet> thymeleafServletBean() {
		ServletRegistrationBean<ThymeleafServlet> bean = new ServletRegistrationBean<>(new ThymeleafServlet(), "/thymeleafServlet/*");
		bean.setLoadOnStartup(1);
		return bean;
	}

    public static void main(String[] args) {
		System.setProperty("spring.devtools.restart.enabled", "false");
        SpringApplication.run(ServingWebContentApplication.class, args);
    }

}