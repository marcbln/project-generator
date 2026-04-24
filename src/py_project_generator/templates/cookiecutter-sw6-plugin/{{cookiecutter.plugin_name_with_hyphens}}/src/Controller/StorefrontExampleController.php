<?php declare(strict_types=1);

namespace {{ cookiecutter.namespace }};

use Shopware\Core\Framework\Routing\Annotation\RouteScope;
use Shopware\Storefront\Controller\StorefrontController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

#[RouteScope(scopes: ['storefront'])]
class StorefrontExampleController extends StorefrontController
{
    #[Route(
        path: '/{{ cookiecutter.plugin_name_with_hyphens }}/example', 
        name: 'frontend.{{ cookiecutter.plugin_name_with_hyphens }}.example', 
        methods: ['GET']
    )]
    public function exampleAction(): Response
    {
        return $this->renderStorefront('@{{ cookiecutter.namespace.split('\\\\')[1] }}/storefront/example.html.twig', [
            'pluginName' => '{{ cookiecutter.plugin_name }}'
        ]);
    }
}
